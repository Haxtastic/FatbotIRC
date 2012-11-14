import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser

class protocolIRC():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.read_config()
		
	def prase_privmsg(self, event):
		source = event.source
		channel = event.channel
		message = event.message
		
		# :Kek!Keke@somekind.ofspecial.mask PRIVMSG Fatbot :Hey
		if message.find(" ") == -1 or not self.is_master(source.split("!")[1]):  # If no parameters or not master, discard
			return
		command = message.split(" ")
		parameters = command[1:]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		
		if command == "join":  # channel
			self.evManager.post(JoinEvent(parameters[0]))
		elif command == "part":  # channel
			self.evManager.post(PartEvent(parameters[0]))
		elif command == "send":  # destination, message
			#parameters = parameters.split(" ", 1)
			self.evManager.post(SendPrivmsgEvent(parameters[0], parameters[1]))
		elif command == "reloadconfig":  # list of modules to reload
			for module in parameters:
				self.evManager.post(ReloadconfigEvent(module))
		
	def notify(self, event):
		if isinstance(event, PrivmsgEvent):
			self.prase_privmsg(event)
		elif isinstance(event, ReloadconfigEvent):
			if event.module == "protocolirc" or event.module == "all":
				self.read_config()
				
	def is_master(self, source):
		print source
		for master in self.masters:
			print master
			if source.lower() == master.lower():
				return True
		return False
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.masters = self.config.get("protocolirc", "masters").strip(" ").split(",")
			