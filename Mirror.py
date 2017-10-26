# -*- coding: utf-8 -*-
import logging

from libs import Display
from libs import Weather
from libs import News
from libs import Schedule
from libs.Rfid import Rfid, hex2str
from libs import Database
import peewee
import random
import time
from threading import Timer, Thread
from ConfigParser import ConfigParser

config = ConfigParser()

weather = Weather.Weather()
news = News.News()
schedule = Schedule.Schedule()
rfid = Rfid()
Database._db.close()
timer = None


def updater():
    global weather, news, timer

    context = {}

    weather.requestWeather()
    context.update(weather.get())

    news.requestNews()
    context.update({'news': news.get(4)})

    screen.invoke_in_main_thread(screen.display, 'main.html', context)

    timer = Timer(6 * 60 * 60, updater, ())
    timer.start()


def renderSchedule(_for):
    global news, weather, schedule
    context = {"random_cat": random.randint(1, 10)}
    screen.invoke_in_main_thread(screen.display, 'loading.html', context)

    start_time = time.time()

    context = {}

    type = "LE"
    schData = schedule.requestSchedule(Rfid.mifareDataToInt(_for))
    if (not schData or schData == None):
        type = "BE"
        schData = schedule.requestSchedule(Rfid.reversedMifareDataToInt(_for))

    if (not schData or schData == None):
        type = "NULL"

    try:
        Database.StatsModel.create(mifare=hex2str(_for), type=type)
    except peewee.IntegrityError:
        pass
    except peewee.OperationalError:
        pass

    context.update({'schedule_data': schData, 'fill_zero': lambda x: ("%02d" % x)})

    if (time.time() - start_time) < 2:
        time.sleep(2)  # give kittens more time to display :D

    if (schData == None):
        screen.invoke_in_main_thread(screen.display, 'error.html', context)
    else:
        screen.invoke_in_main_thread(screen.display, 'schedule.html', context)

    time.sleep(5)

    context = {}

    context.update(weather.get())
    context.update({'news': news.get(4)})

    screen.invoke_in_main_thread(screen.display, 'main.html', context)


def reader():
    global rfid

    rfid.scan(renderSchedule)


if __name__ == "__main__":
    config.readfp(open('config.ini'))

    logger = logging.getLogger('peewee')
    logger.setLevel(logging.ERROR)

    Database.StatsModel.create_table(fail_silently=True)

    if config != None:
        if config.has_option('Mirror', 'weather_api_key'):
            Weather.Weather.OWAPI_KEY = config.get('Mirror', 'weather_api_key')

        if config.has_option('Mirror', 'schedule_api_url'):
            Schedule.Schedule.SCHAPI_URL = config.get('Mirror', 'schedule_api_url')

        if config.has_option('Mirror', 'schedule_api_login') and config.has_option('Mirror', 'schedule_api_password'):
            schedule.setCredentials(config.get('Mirror', 'schedule_api_login'),
                                    config.get('Mirror', 'schedule_api_password'))

    app = Display.QtApp()

    screen = Display.Screen()
    screen.showFullScreen()

    updater()

    Thread(target=reader).start()

    app.execute()

    if timer:
        timer.cancel()

    rfid.close()
