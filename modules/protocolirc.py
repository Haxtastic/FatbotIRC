import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser
from weakboundmethod import WeakBoundMethod as Wbm

class protocolirc():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self.started = False;
		self._connections = [
			self.ed.add(PrivmsgEvent, Wbm(self.parse_privmsg)),
			self.ed.add(ReloadconfigEvent, Wbm(self.reload_config))
		]
		
	def parse_privmsg(self, event):
		if self.started == False:
			return
		nick, source = event.source.split("!")
		channel = event.channel
		message = event.message
		
		# :Kek!Keke@somekind.ofspecial.mask PRIVMSG Fatbot :Hey
		if channel[0] == "#" or message.find(" ") == -1 or not self.is_master(source):  # If no parameters or not master, discard
			return
		command = message.split(" ")
		parameters = command[1:]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		
		if command == "join":  # channel
			self.ed.post(JoinEvent(parameters[0], nick))
		elif command == "part":  # channel
			self.ed.post(PartEvent(parameters[0], nick))
		elif command == "send":  # destination, message
			text = ""
			for word in parameters[1:]:
				text += "%s " % (word, )
			self.ed.post(SendPrivmsgEvent(parameters[0], text.strip(), nick))
		elif command == "reloadconfig":  # list of modules to reload
			for module in parameters:
				self.ed.post(ReloadconfigEvent(module, nick))
		elif command == "disconnect" or command == "reconnect":
			text = ""
			for word in parameters:
				text += "%s " % (word, )
			text.strip()
			if command == "disconnect":
				self.ed.post(DisconnectEvent(text, nick))
			elif command == "reconnect":
				self.ed.post(ReconnectEvent(text, nick))
			return
		elif command == "print":
			self.ed.post(ListenerPrintEvent())
			
	def reload_config(self, event):
		if event.module == "protocolirc" or event.module == "all":
			self.read_config()			

	def is_master(self, source): # checks if source is master
		for master in self.masters:
			if source.lower() == master.lower():
				return True
		return False
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.masters = self.config.get("protocolirc", "masters").replace(" ", "").split(",")
			