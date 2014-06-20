import thread
import ConfigParser
from connection import Connection
from consoleview import ConsoleView
from events import *
import os, sys
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)
from moduleloader import load_modules, reload_modules
from weakboundmethod import WeakBoundMethod as Wbm

"""
Our main bot class. This is where we load modules, change the state of the bot, connect to the server etc.
Actually quite a simple class, but it does what it should.
"""

class Bot:
	STATE_STOPPED = 'stopped'
	STATE_PREPARING = 'preparing'
	STATE_RUNNING = 'running'
	STATE_PAUSED = 'paused'

	def __init__(self, ed):
		self.ed = ed
		self.config = ConfigParser.RawConfigParser()
		self.read_config()
		self.state = Bot.STATE_STOPPED
		self._connections = [
			self.ed.add(StartEvent, Wbm(self.start)),
			self.ed.add(ConnectedEvent, Wbm(self.connected)),
			self.ed.add(WelcomeEvent, Wbm(self.start_modules)),
			self.ed.add(ReloadconfigEvent, Wbm(self.reload_config)),
			self.ed.add(ConnectionClosedEvent, Wbm(self.connection_closed))
		]
	
	
	def start(self, event):
		self.state = Bot.STATE_PREPARING
		self.console = ConsoleView(self.ed)
		self.modules = load_modules(self.ed)
		self.server = Connection(self.ip, self.port, self.ed)
		self.server.connect(self.ssl)
	
	def start_modules(self, event):
		for module in self.modules:
			if hasattr(module, "started"):
				module.started = True
		if(self.state == Bot.STATE_PREPARING):
			self.state = Bot.STATE_RUNNING
			self.ed.post(RunningEvent())
	
	def connected(self, event):
		self.ed.post(LoginEvent(self.name))
	
	def reload_config(self, event):
		if event.module == "core" or event.module == "all":
			self.read_config()
		if event.module == "modules":
			print "#### reload_modules called ####"
			#self.modules = 
			reload_modules(self.modules, self.ed)
			print "#### reload_modules returns ####"
			print self.modules
	
	def connection_closed(self, event):
		self.state = Bot.STATE_STOPPED
		self.ed.post(QuitEvent())
	
	def read_config(self):
		self.config.read('config.cfg')
		self.ip   	= self.config.get		("Connection", "ip")
		self.port 	= self.config.getint	("Connection", "port")
		self.name 	= self.config.get		("Connection", "name")
		self.ssl 	= self.config.getint	("Connection", "ssl")
			