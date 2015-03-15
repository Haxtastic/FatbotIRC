import os, sys
from core.events import *
import ConfigParser
from core.weakboundmethod import WeakBoundMethod as Wbm
from core.botinfo import read_config_section

class nickserv():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self._connections = [
			self.ed.add(ReginfoEvent, Wbm(self.identify)),
			self.ed.add(NoticeEvent, Wbm(self.hostmask))
		]
		
	def identify(self, event):
		if event.type != "001":
			return
		if "quakenet" in event.source:
			RequestSendPrivmsgEvent("Q@Cserve.quakenet.org", "auth %s %s" % (self.nick, self.password)).post(self.ed)
		elif "dream-irc" in event.source:
			RequestSendPrivmsgEvent("nickserv", "identify %s" % (self.password, ), "").post(self.ed)
		else:
			RequestSendPrivmsgEvent("nickserv", "identify %s %s" % (self.nick, self.password), "").post(self.ed)
			
	def hostmask(self, event):
		if "are now logged in" not in event.data:
			return
		name = event.dest
		RequestSendCommandEvent("MODE", "%s +x" % name, "").post(self.ed)
			
	def read_config(self):
		config = read_config_section(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'), "nickserv")
		self.nick = config["nick"]
		self.password = config["password"]
