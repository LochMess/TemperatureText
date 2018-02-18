#####
# Class TelstraSMS is built using the Telstra Messaging API python SDK version 1.0.2 (https://github.com/telstra/MessagingAPI-SDK-python) to allow sms messages to be sent via Telstra's API.
#####

from __future__ import print_function
import time
import Telstra_Messaging
from Telstra_Messaging.rest import ApiException
from pprint import pprint
import configparser
from datetime import datetime, timedelta
import re

class TelstraSMS:
    'Class for sending SMS via TelstraAPI'

    instanceCount = 0

    def __init__(self,configPath):
        config = configparser.ConfigParser()
        config.read(configPath+'config.ini')
        TelstraAPIConfig = config['TelstraMessagingAPICredentials']

        self.client_id = TelstraAPIConfig['Id']
        self.client_secret = TelstraAPIConfig['Secret']
        self.grant_type = TelstraAPIConfig['GrantType']
        self.authToken = None
        self.authTokenExpiry = None
        self.provisionInstance = None
        self.configuration = None

        TelstraSMS.instanceCount += 1

    def __str__(self):
        return re.sub('  +','','''
            client_id = {0}
            client_secret = {1}
            grant_type = {2}
            authToken = {3}
            authTokenExpiry = {4}
            provisionInstance Exists = {5}
            configuration Exists = {6}'''.format(self.client_id, self.client_secret, self.grant_type, self.authToken, self.authTokenExpiry, self.provisionInstance is not None, self.configuration is not None))

    def __checkAuthToken(self):
        'Check whether an OAuth 2.0 token exists or is current and get one if required.'

        if self.authToken is None or self.authTokenExpiry <= datetime.now():
            self.generateAuthToken()

    def generateAuthToken(self):
        'Uses the Telstra messaging API client credientals to get an OAuth 2.0 token.'

        api_instance_Auth = Telstra_Messaging.AuthenticationApi()
        try:
            self.authToken = api_instance_Auth.auth_token(self.client_id, self.client_secret, self.grant_type)
            self.authTokenExpiry = datetime.now() + timedelta(seconds=3598)
            pprint(self.authToken)
        except ApiException as e:
            print("Exception when calling AuthenticationApi->auth_token: %s\n" % e)

        self.configuration = Telstra_Messaging.Configuration()
        self.configuration.access_token = self.authToken.access_token
        self.provisionInstance = Telstra_Messaging.ProvisioningApi(Telstra_Messaging.ApiClient(self.configuration))

    def createSubscription(self, length = None):
        'Creates a subscription with the Telstra API, ie gets a mobile number to use. length defines the number of days to create the subscription for, no value will default to API default.'

        self.__checkAuthToken()
        body = Telstra_Messaging.ProvisionNumberRequest(length)
        try:
            api_response = self.provisionInstance.create_subscription(body)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ProvisioningApi->create_subscription: %s\n" % e)

    def getSubscription(self):
        'Checks the status of the subscription, ie what the mobile number and how long is left on the subscription.'

        self.__checkAuthToken()
        try:
            api_response = self.provisionInstance.get_subscription()
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ProvisioningApi->get_subscription: %s\n" % e)

    def deleteSubscription(self):
        'Deletes the subscription, ie releases the mobile number in use.'

        self.__checkAuthToken()
        body = Telstra_Messaging.DeleteNumberRequest()
        try:
            self.provisionInstance.delete_subscription(body)
        except ApiException as e:
            print("Exception when calling ProvisioningApi->delete_subscription: %s\n" % e)

    def sendSMS(self, recipient, message):
        'Sends a SMS to the given recipient with the given message.'

        self.__checkAuthToken()
        api_instance_Messaging = Telstra_Messaging.MessagingApi(Telstra_Messaging.ApiClient(self.configuration))
        payload = Telstra_Messaging.SendSMSRequest(recipient, message)
        try:
            api_response = api_instance_Messaging.send_sms(payload)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling MessagingApi->send_sms: %s\n" % e)
