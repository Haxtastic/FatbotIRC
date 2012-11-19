import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser

class protocolIRC():
	def __init__(self, evManager):
		self.evManager = evManager
		self.read_config()
		self.started = False;
		self.evManager.register_listener(self)
		
	def parse_privmsg(self, event):
		if self.started == False:
			return
		source = event.source
		channel = event.channel
		message = event.message
		
		# :Kek!Keke@somekind.ofspecial.mask PRIVMSG Fatbot :Hey
		if channel[0] == "#" or message.find(" ") == -1 or not self.is_master(source.split("!")[1]):  # If no parameters or not master, discard
			return
		command = message.split(" ")
		parameters = command[1:]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		
		if command == "join":  # channel
			self.evManager.post(JoinEvent(parameters[0]))
		elif command == "part":  # channel
			self.evManager.post(PartEvent(parameters[0]))
		elif command == "send":  # destination, message
			text = ""
			for word in parameters[1:]:
				text += "%s " % (word, )
			text.strip()
			self.evManager.post(SendPrivmsgEvent(parameters[0], text))
		elif command == "reloadconfig":  # list of modules to reload
			for module in parameters:
				self.evManager.post(ReloadconfigEvent(module))
		elif command == "disconnect":
			text = ""
			for word in parameters:
				text += "%s " % (word, )
			text.strip()
			self.evManager.post(DisconnectEvent(text))
			return
		
	def notify(self, event):
		if isinstance(event, PrivmsgEvent):
			self.parse_privmsg(event)
		elif isinstance(event, ReloadconfigEvent):
			if event.module == "protocolirc" or event.module == "all":
				self.read_config()
		elif isinstance(event, WelcomeEvent):
			self.started = True

	def is_master(self, source):
		for master in self.masters:
			if source.lower() == master.lower():
				return True
		return False
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.masters = self.config.get("protocolirc", "masters").replace(" ", "").split(",")
			