from WeatherScraper import WeatherScraper
from TelstraSMS import TelstraSMS
from pprint import pprint
from statistics import mean
import configparser

ConfigPath = 'TemperatureText/'
scrapeError = ''
config = configparser.ConfigParser()
config.read(ConfigPath+'config.ini')
AlertConfig = config['Alert']
SitesConfig = config['Sites']

temperatureList = list()
weatherSources = list()
for x in range(len(SitesConfig['Url'].split(','))):
    weatherSources.append(WeatherScraper(SitesConfig['Url'].split(',')[x],SitesConfig['Element'].split(',')[x],SitesConfig['Attribute'].split(',')[x],SitesConfig['AttributeValue'].split(',')[x]))
    weatherSources[x].checkCurrentWeather()
    if weatherSources[x].currentWeather is not None:
        temperatureList.append(float(weatherSources[x].currentWeather))
    else:
        scrapeError = scrapeError+' Weather was unavailable from '+weatherSources[x].siteName+'.'

averageTemperature = mean(temperatureList)

if averageTemperature > int(AlertConfig['TempThreshold']):
    messenger = TelstraSMS(ConfigPath)
    messenger.createSubscription()
    messenger.sendSMS(AlertConfig['Recipient'], AlertConfig['MessagePrecedingTemp']+' '+str(averageTemperature)+'. '+AlertConfig['MessageFollowingTemp']+' '+scrapeError)
