# -*- coding: utf-8 -*-
import logging

from libs import Display
from libs import Weather
from libs import News
from libs import Schedule
from libs.Rfid import Rfid, hex2str
from libs import Database
import peewee
import random, os
import time, datetime
from threading import Timer, Thread
from ConfigParser import ConfigParser

timer = None
timerInfo = None
layout = "mirror"

def updater():
    global weather, news, timer

    context = {}

    weather.requestWeather()
    news.requestNews()

    renderHome()

    timer = Timer(3 * 60 * 60, updater)
    timer.start()

def renderHome():
    global timerInfo
    context = {}

    context.update(weather.get())
    context.update({'news': news.get(4)})

    screen.invoke_in_main_thread(screen.display, layout + '/main.html', context)

    if timerInfo:
        timerInfo.cancel()
        timerInfo = None

    timerInfo = Timer(60, renderInfo)
    timerInfo.start()

def renderInfo():
    global timerInfo
    context = {}

    screen.invoke_in_main_thread(screen.display, layout + '/info.html', context)

    if timerInfo:
        timerInfo.cancel()
        timerInfo = None

    timerInfo = Timer(15, renderHome)
    timerInfo.start()


def renderSchedule(_for):
    global news, weather, schedule, timerInfo
    screen.display_icon(screen.icons[2])  # sync

    if timerInfo:
        timerInfo.cancel()
        timerInfo = None

    context = {"random_cat": random.randint(1, 15)}
    screen.invoke_in_main_thread(screen.display, layout + '/loading.html', context)

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
    now = datetime.datetime.now().strftime("%d.%m.%Y r. %H:%M")
    context.update({ 'now': now })

    if (time.time() - start_time) < 2:
        time.sleep(time.time() - start_time)  # give kittens more time to display :D

    if (schData == None):
        screen.invoke_in_main_thread(screen.display, layout + '/error.html', context)
    else:
        screen.invoke_in_main_thread(screen.display, layout + '/schedule.html', context)

    time.sleep(5)
    screen.hide_icon()
    renderHome()

def reader():
    global rfid
    rfid.scan(renderSchedule)

if __name__ == "__main__":
    config = ConfigParser()
    config.readfp(open('config.ini'))

    logger = logging.getLogger('peewee')
    logger.setLevel(logging.ERROR)

    app = Display.QtApp()

    screen = Display.Screen()
    screen.showFullScreen()
    screen.load_icons()

    weather = Weather.Weather()
    news = News.News()
    schedule = Schedule.Schedule(screen)
    rfid = Rfid()

    Database._db.close()
    Database.StatsModel.create_table(fail_silently=True)

    if config != None:
        if config.has_option('Mirror', 'weather_api_key'):
            Weather.Weather.OWAPI_KEY = config.get('Mirror', 'weather_api_key')

        if config.has_option('Mirror', 'schedule_api_url'):
            Schedule.Schedule.SCHAPI_URL = config.get('Mirror', 'schedule_api_url')

        if config.has_option('Mirror', 'schedule_api_login') and config.has_option('Mirror', 'schedule_api_password'):
            schedule.setCredentials(config.get('Mirror', 'schedule_api_login'),
                                    config.get('Mirror', 'schedule_api_password'))

        if config.has_option('Mirror', 'mirror_layout'):
            lay = config.get('Mirror', 'mirror_layout')
            if os.path.isdir(os.path.join("templates/", layout)):
                layout = lay

    updater()

    Thread(target=reader).start()

    app.execute()

    if timer:
        timer.cancel()

    rfid.close()
