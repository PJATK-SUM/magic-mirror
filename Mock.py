# -*- coding: utf-8 -*-
from libs import Display
from libs import Schedule
import datetime, random

layout = "kiosk"

def sch():
    schData = schedule.requestSchedule(12690)
    context = {}
    context.update({'schedule_data': schData, 'fill_zero': lambda x: ("%02d" % x)})
    now = datetime.datetime.now().strftime("%d.%m.%Y r. %H:%M")
    context.update({'now': now})
    screen.invoke_in_main_thread(screen.display, layout + '/schedule.html', context)

def error():
    screen.invoke_in_main_thread(screen.display, layout + '/error.html', {})

def main():
    context = {}
    context.update({
            'temperature': 13,
            'icon_class': 'wi-day-cloudy',
            'description': 'mało chmur'
        })
    context.update({'news': [{
                    'title': "Lorem ipsum dolor sit amet",
                    'content': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec semper, metus non bibendum commodo, nisl nulla finibus eros, nec porta sem ipsum sit amet neque. Praesent venenatis gravida neque non aliquet. Nunc nec urna odio. Donec aliquet est vitae scelerisque consequat. Praesent lacinia ante libero, volutpat aliquam erat porta sit amet. Aenean mattis, urna non rutrum finibus, lectus tortor eleifend nisl, vitae porttitor eros lorem vitae magna. Sed et dolor tortor. Nunc sapien arcu, luctus vitae facilisis sit amet, dapibus et enim. Nam vulputate leo eu tellus condimentum vehicula.",
                    'date': "00-00-0000"
                } for i in range(4)]})

    screen.invoke_in_main_thread(screen.display, layout + '/main.html', context)

def loading():
    context = {"random_cat": random.randint(1, 15)}
    screen.invoke_in_main_thread(screen.display, layout + '/loading.html', context)

if __name__ == "__main__":
    app = Display.QtApp()

    screen = Display.Screen()
    screen.showFullScreen()
    screen.load_icons()

    schedule = Schedule.Schedule(screen)
    schedule.setCredentials("", "")

    main()

    app.execute()

