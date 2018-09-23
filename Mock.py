# -*- coding: utf-8 -*-
from libs import Display
from libs import Schedule
import datetime

schedule = Schedule.Schedule()

def rednder():
    schData = schedule.requestSchedule(12690)
    context = {}
    context.update({'schedule_data': schData, 'fill_zero': lambda x: ("%02d" % x)})
    now = datetime.datetime.now().strftime("%d.%m.%Y r. %H:%M")
    context.update({'now': now})
    screen.invoke_in_main_thread(screen.display, 'new-schedule.html', context)

if __name__ == "__main__":
    app = Display.QtApp()

    screen = Display.Screen()
    screen.showFullScreen()

    schedule.setCredentials("", "")
    rednder()

    app.execute()
