import urllib.request
from bs4 import BeautifulSoup
import re
from datetime import datetime

class WeatherScraper:
    'class for scraping given weather sites and attributes to retrieve current weather'

    numberSources = 0

    def __init__(self, site, element, attribute, attributeValue):
        self.site = site
        self.siteName = site.split('.')[1]
        self.element = element
        self.attribute = attribute
        self.attributeValue = attributeValue
        self.currentWeather = None
        self.lastUpdate = None
        self.error = None

        WeatherScraper.numberSources += 1

    def checkCurrentWeather(self):
        page = urllib.request.urlopen(self.site)
        self.lastUpdate = datetime.now()
        soup = BeautifulSoup(page, 'html.parser')
        target = soup.find(self.element, attrs={self.attribute:self.attributeValue}).text.strip()
        self.currentWeather = re.sub('[^\d.]+', '', target)
        if (-100<=float(self.currentWeather) and float(self.currentWeather)>=100):
            self.error = target
            self.currentWeather = None
            return self.error
        else:
            return self.currentWeather
