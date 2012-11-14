import thread
import ConfigParser
from connection import Connection
from consoleview import ConsoleView
from events import *
import os, sys
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)
from moduleloader import load_modules

class Bot:
	STATE_PREPARING = 'preparing'
	STATE_RUNNING = 'running'
	STATE_PAUSED = 'paused'

	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.read_config()
		#self.name = name
		#self.ip = ip
		#self.port = port
		self.state = Bot.STATE_PREPARING


	def start(self):
		self.console = ConsoleView(self.evManager)
		self.evManager.post(ConsoleEvent("Starting up..."))
		self.server = Connection(self.ip, self.port, self.evManager)
		thread.start_new_thread(self.server.connect, ())
		self.modules = load_modules(self.evManager)
		self.state = Bot.STATE_RUNNING

	def notify(self, event):
		if isinstance(event, TickEvent):
			if(self.state == Bot.STATE_PREPARING):
				self.start()
		elif isinstance(event, ConnectedEvent):
			self.evManager.post(LoginEvent(self.name))
				
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read('config.cfg')
		self.ip = 		self.config.get("Login", "ip")
		self.name = 	self.config.get("Login", "name")
		self.port = 	self.config.getint("Login", "port")
			