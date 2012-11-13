import thread
from connection import Connection
from events import *
import random
import time

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
			
		self.state = Bot.STATE_RUNNING
		
	def prase_privmsg(self, event):
		source = event.source
		channel = event.channel
		message = event.message
		command = event.command
		parameters = event.parameters
		
		if command == "join": #Channel
			self.evManager.post(JoinEvent(parameters))
		if command == "send": #Channel, message
			parameters = parameters.split(" ", 1)
			self.evManager.post(SendPrivmsgEvent(parameters[0], parameters[1]))
	

	def notify(self, event):
		if isinstance(event, TickEvent):
			if(self.state == Bot.STATE_PREPARING):
				self.start()
		if isinstance(event, PrivmsgEvent):
			self.prase_privmsg(event)