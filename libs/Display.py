# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtCore
from PySide import QtGui, QtWebKit
from jinja2 import Environment, FileSystemLoader

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

	def __init__(self, templatesDir = 'templates', resourcesDir = 'resources'):
		super(Screen, self).__init__(parent=None, flags=0)

		reload(sys)
		sys.setdefaultencoding('utf-8')

		self._resUrl = "file:///%s/%s" % (os.path.dirname(os.path.abspath(__file__ + '/../')), resourcesDir)
		
		self.env = Environment(loader = FileSystemLoader("./%s/" % (templatesDir)))
		layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)

		self.web_app = QtWebKit.QWebView()
		
		self.setCentralWidget(self.web_app)
		
		self.web_app.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
		self.web_app.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
		self.web_app.setTextSizeMultiplier(0.85)
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

	def keyPressEvent(self, e):
		if(e.key() == QtCore.Qt.Key_Escape):
			self.close()
			
	def display(self, template, context):
		tpl = self.env.get_template(template)
		context['resources'] = self._resUrl
		self.web_app.setHtml(tpl.render(**context))

	def invoke_in_main_thread(self, fn, *args, **kwargs):
		QtCore.QCoreApplication.postEvent(self._invoker, InvokeEvent(fn, *args, **kwargs))