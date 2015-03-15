import thread, atexit, random
import ConfigParser
from connection import Connection
from consoleview import ConsoleView
from events import *
from botinfo import read_config_section
import os, sys
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)
import moduleloader
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
			self.ed.add(ConnectedEvent, Wbm(self.start_modules)),
			self.ed.add(ReloadconfigEvent, Wbm(self.reload_config)),
			self.ed.add(ConnectionClosedEvent, Wbm(self.connection_closed))
		]
		self.read_config()
		self.console = ConsoleView(self.ed)
		self.server = Connection(self.ip, self.port, self.ed)
		self.server.connect(self.ssl)
	
	def start_modules(self, event):
		self.modules = moduleloader.load_modules(self.ed)
		LoginEvent(self.name).post(self.ed)
	
	def reload_config(self, event):
		if event.module == "core" or event.module == "all":
			self.read_config()
		if event.module == "modules":
			self.modules = []
			reload(moduleloader)
			self.modules = moduleloader.reload_modules(self.modules, self.ed)
	
	def connection_closed(self, event):
		if (event.type == "server" and self.reconnect) or event.type == "reconnect":
			self.restart()
		else:
			QuitEvent().post(self.ed)

	def restart(self):
		self._connections = None
		self.config = None
		self.modules = None
		self.server = None
		self.start()
	
	def read_config(self):
		config = read_config_section(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.cfg"), "Connection")
		self.ip			= config["prefix"][1] + config["ip"]#random.choice(config["prefix"]) + config["ip"]
		self.port 		= config["port"][2]#random.choice(config["port"])
		self.name 		= config["name"]
		self.ssl 		= config["ssl"]
		self.reconnect	= config["reconnect"]

