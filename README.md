# Temperature Text
Small project in python to scrape current temperature and send a sms message via Telstra's messaging API (https://dev.telstra.com/content/messaging-api).

## Setup
This program was written in python 3.5.1, with the Telstra messaging API python SDK.

Install the Telstra messaging API python SDK.

`pip install git+https://github.com/Telstra/MessagingAPI-SDK-python.git`

(You can find out more about this SDK here, https://github.com/telstra/MessagingAPI-SDK-python)

The other packages and libraries are mostly common packages and libraries, but if you do not have one or more of them just install it via pip.

## Configuration
Rename 'TEMPLATE config.ini' to 'config.ini' and replace the comments including the hashes surrounding them with the required data the id and secret from your Telstra API key, and a valid mobile phone number. These are the fields that must be edited before use, the other fields maybe edited as desired.

Within the Main.py file, set the absolute path for the config.ini file, edit the ConfigPath variable on line 7, an example of this is included in the example below.

## Example Run as an hourly cronjob on Ubuntu
Ubuntu has python 2.7 installed for older code as well as python 3.5, so python 3.5 is called via python3 in the terminal.

Install pip for python3 on Ubuntu and update it to the latest version,

```
sudo apt install python3-pip
pip3 install --upgrade pip
```

Navigate to the directory where you want this script to reside and clone this repo,

`git clone https://github.com/LochMess/TemperatureText`

Install the Telstra messaging API python SDK,

`pip3 install git+https://github.com/Telstra/MessagingAPI-SDK-python.git`

Set the absolute path for the config.ini file in Main.py on line 7, if your username was Bob that might look something like this,

`ConfigPath = '/home/bob/scripts/TemperatureText/'`

Now add it as a cronjob to be ran hourly,

```
crontab -e

0 * * * * python3 /home/bob/scripts/TemperatureText/Main.py
```

Alternatively the output generated by the script can be sent to a file by instead using the following cronjob.

`0 * * * * python3 /home/bob/scripts/TemperatureText/Main.py >> /home/bob/scripts/TemperatureText/cronOutput.txt 2>&1`
