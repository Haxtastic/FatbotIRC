import thread
from connection import Connection
from events import *
import os, sys
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)
from moduleloader import load_modules

class Bot:
	STATE_PREPARING = 'preparing'
	STATE_RUNNING = 'running'
	STATE_PAUSED = 'paused'

	def __init__(self, name, ip, port, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.server = []
		self.name = name
		self.ip = ip
		self.port = port
		self.state = Bot.STATE_PREPARING
		self.modules = []


	def start(self):
		server = Connection(self.ip, self.port, self.evManager)
		thread.start_new_thread(server.connect, (self.name,))
		self.modules = load_modules(self.evManager)
		self.state = Bot.STATE_RUNNING	

	def notify(self, event):
		if isinstance(event, TickEvent):
			if(self.state == Bot.STATE_PREPARING):
				self.start()
			