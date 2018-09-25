# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtCore
from PySide import QtGui, QtWebKit
from jinja2 import Environment, FileSystemLoader

icons = ["resources/images/icons/upload.png",  # 0
         "resources/images/icons/download.png",  # 1
         "resources/images/icons/sync.png",  # 2
         "resources/images/icons/empty.png",  # 3
         "resources/images/icons/error.png",  # 4
         "resources/images/icons/ok.png"]  # 5

class QtApp:
    def __init__(self):
        self.app = QtGui.QApplication.instance()
        if self.app is not None:
            raise RuntimeError("Another QT application is already running")
        elif self.app is None:
            self.app = QtGui.QApplication(sys.argv)

    def execute(self):
        self.app.exec_()


class InvokeEvent(QtCore.QEvent):
    EVENT_TYPE = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

    def __init__(self, fn, *args, **kwargs):
        QtCore.QEvent.__init__(self, InvokeEvent.EVENT_TYPE)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs


class Invoker(QtCore.QObject):
    def event(self, event):
        event.fn(*event.args, **event.kwargs)

        return True


class Screen(QtGui.QMainWindow):
    _invoker = Invoker()

    web_app = None
    icon = None
    icons = None

    def __init__(self, templatesDir='templates', resourcesDir='resources'):
        super(Screen, self).__init__(parent=None, flags=0)

        reload(sys)
        sys.setdefaultencoding('utf-8')
        self._resUrl = "file:///%s/%s" % (os.path.dirname(os.path.abspath(__file__ + '/../')), resourcesDir)

        self.env = Environment(loader=FileSystemLoader("./%s/" % (templatesDir)))
        layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)

        self.web_app = QtWebKit.QWebView()

        self.setCentralWidget(self.web_app)

        self.icon = QtGui.QLabel(self.web_app)
        self.icon.setBackgroundRole(QtGui.QPalette.Base)
        self.icon.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.icon.setScaledContents(True)
        self.icon.show()

        self.web_app.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.web_app.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
        self.web_app.setTextSizeMultiplier(0.85)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def load_icons(self):
        self.icons = []
        for p in icons:
            self.icons.append(QtGui.QPixmap(p))

    def keyPressEvent(self, e):
        if (e.key() == QtCore.Qt.Key_Escape):
            self.close()

    def display_icon(self, icon):
        self.invoke_in_main_thread(self.__display_icon, icon)

    def __display_icon(self, icon):
        self.icon.setPixmap(icon)
        self.icon.setGeometry(self.web_app.width() - 58, self.web_app.height() - 58, 48, 48)
        self.icon.adjustSize()
        self.icon.repaint()

    def hide_icon(self):
        self.invoke_in_main_thread(self.icon.hide)

    def display(self, template, context):
        tpl = self.env.get_template(template)
        context['resources'] = self._resUrl
        html = tpl.render(**context)
        #print html
        self.web_app.setHtml(html)

    def invoke_in_main_thread(self, fn, *args, **kwargs):
        QtCore.QCoreApplication.postEvent(self._invoker, InvokeEvent(fn, *args, **kwargs))
