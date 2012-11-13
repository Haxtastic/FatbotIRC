import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *

class PrivmsgPraser():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		
	def prase_privmsg(self, event):
		source = event.source
		channel = event.channel
		message = event.message
		command = event.command
		parameters = event.parameters
		
		if command == "join":  # channel
			self.evManager.post(JoinEvent(parameters))
		if command == "send":  # destination, message
			parameters = parameters.split(" ", 1)
			self.evManager.post(SendPrivmsgEvent(parameters[0], parameters[1]))
		
	def notify(self, event):
		if isinstance(event, PrivmsgEvent):
			self.prase_privmsg(event)