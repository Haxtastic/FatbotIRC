import thread, atexit
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

	def __init__(self, ed):
		self.ed = ed
	
	def start(self):
		self._connections = [
			self.ed.add(ConnectedEvent, Wbm(self.connected)),
			self.ed.add(WelcomeEvent, Wbm(self.start_modules)),
			self.ed.add(ReloadconfigEvent, Wbm(self.reload_config)),
			self.ed.add(ConnectionClosedEvent, Wbm(self.connection_closed))
		]
		self.config = ConfigParser.RawConfigParser()
		self.read_config()
		self.console = ConsoleView(self.ed)
		self.server = Connection(self.ip, self.port, self.ed)
		self.server.connect(self.ssl)
	
	def start_modules(self, event):
		self.modules = load_modules(self.ed)
		self.ed.post(RunningEvent(self.ip))
	
	def connected(self, event):
		self.ed.post(LoginEvent(self.name))
	
	def reload_config(self, event):
		if event.module == "core" or event.module == "all":
			self.read_config()
		if event.module == "modules":
			reload_modules(self.modules, self.ed)
	
	def connection_closed(self, event):
		if (event.type == "server" and self.reconnect) or event.type == "reconnect":
			self.restart()
		else:
			self.ed.post(QuitEvent())

	def restart(self):
		self._connections = None
		self.config = None
		self.console = None
		self.modules = None
		self.server = None
		self.start()
	
	def read_config(self):
		self.config.read('config.cfg')
		self.ip   		= self.config.get		("Connection", "ip")
		self.port 		= self.config.getint	("Connection", "port")
		self.name 		= self.config.get		("Connection", "name")
		self.ssl 		= self.config.getint	("Connection", "ssl")
		self.reconnect	= self.config.getint	("Connection", "reconnect")

