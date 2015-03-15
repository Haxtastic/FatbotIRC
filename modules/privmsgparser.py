import os, sys
#lib_path = os.path.abspath(os.path.join("..", "core"))
#sys.path.append(lib_path)
from core.events import *
import ConfigParser
from core.weakboundmethod import WeakBoundMethod as Wbm
from core.botinfo import read_config_section

class privmsgparser():
	def __init__(self, ed):
		self.ed = ed
		self._connections = [
			self.ed.add(PrivmsgEvent, Wbm(self.parse_privmsg)),
		]
		
	def parse_privmsg(self, event):
		if " " not in event.data:
			return
		nick, source = event.source.split("!")
		command = event.data.split(" ")
		parameters = command[1:]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		message = event.data.split(":")[1]
		ParsedPrivmsgEvent(nick, source, event.dest, message, command, parameters).post(self.ed)