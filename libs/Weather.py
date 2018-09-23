# -*- coding: utf-8 -*-
import urllib2
import json
from peewee import *
import datetime
import Database


class WeatherModel(Database.BaseModel):
    time = DateTimeField(null=False, default=datetime.datetime.now())
    temperature = CharField(null=False)
    icon_class = CharField(null=False)
    description = CharField(null=False)


class Weather:
    OWAPI_URL = "http://api.openweathermap.org/data/2.5/weather"
    OWAPI_KEY = ""
    ICON_MAPPING = {
        "01d": "wi-day-sunny",
        "02d": "wi-day-sunny-overcast",
        "03d": "wi-day-cloudy",
        "04d": "wi-cloudy",
        "09d": "wi-day-showers",
        "10d": "wi-day-rain",
        "11d": "wi-day-thunderstorm",
        "13d": "wi-day-snow",
        "50d": "wi-day-fog",
        "01n": "wi-night-clear",
        "02n": "wi-night-partly-cloudy",
        "03n": "wi-night-cloudy",
        "04n": "wi-cloudy",
        "09n": "wi-night-showers",
        "10n": "wi-night-rain",
        "11n": "wi-night-thunderstorm",
        "13n": "wi-night-snow",
        "50n": "wi-night-fog"
    }
    DESCRIPTION_MAPPING = {
        "clear sky": "bezchmurnie",
        "few clouds": "mało chmur",
        "scattered clouds": "małe zachmurzenie",
        "broken clouds": "pochmurnie",
        "shower rain": "przelotne deszcze",
        "rain": "deszcz",
        "thunderstorm": "burza",
        "snow": "Śnieg",
        "mist": "mgła"
    }

    def __init__(self, apikey=None):
        if apikey is not None:
            Weather.OWAPI_KEY = apikey
        WeatherModel.create_table(fail_silently=True)
        pass

    def requestWeather(self):
        url = "%s?units=metric&q=Warsaw,pl&APPID=%s" % (Weather.OWAPI_URL, Weather.OWAPI_KEY)
        response = urllib2.urlopen(url).read()
        weatherObj = json.loads(response)
        ret = {
            'temperature': int(weatherObj['main']['temp']),
            'icon_class': Weather.ICON_MAPPING[weatherObj['weather'][0]['icon']],
            'description': Weather.DESCRIPTION_MAPPING.get(weatherObj['weather'][0]['description'], "Zmiennie"),
        }

        try:
            WeatherModel.create(time=datetime.datetime.now(),
                                temperature=ret['temperature'],
                                icon_class=ret['icon_class'],
                                description=ret['description'])
        except IntegrityError:
            pass
        except OperationalError:
            pass

    def get(self):
        ret = {
            'temperature': 0,
            'icon_class': '',
            'description': ''
        }
        try:
            last = WeatherModel.select().order_by(-WeatherModel.time).limit(1).get()
            ret = {
                'temperature': int(last.temperature),
                'icon_class': last.icon_class,
                'description': last.description
            }
        except WeatherModel.DoesNotExist:
            pass
        except OperationalError:
            pass

        return ret
