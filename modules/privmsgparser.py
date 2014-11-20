import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser
from weakboundmethod import WeakBoundMethod as Wbm

class privmsgparser():
	def __init__(self, ed):
		self.ed = ed
		self._connections = [
			self.ed.add(PrivmsgEvent, Wbm(self.parse_privmsg)),
		]
		
	def parse_privmsg(self, event):
		if " " not in event.message:
			return
		nick, source = event.source.split("!")
		command = event.message.split(" ")
		parameters = command[1:]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		message = event.message.split(":")[1]
		self.ed.post(ParsedPrivmsgEvent(nick, source, event.channel, message, command, parameters))