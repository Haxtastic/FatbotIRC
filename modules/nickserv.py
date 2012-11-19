import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser

class nickserv():
	def __init__(self, evManager):
		self.evManager = evManager
		self.read_config()
		self.evManager.register_listener(self)
		
	def identify(self):
		self.evManager.post(SendPrivmsgEvent("nickserv", "identify %s %s" % (self.nick, self.password)))
		
	def notify(self, event):
		if isinstance(event, WelcomeEvent):
			self.identify()
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.nick = self.config.get("nickserv", "nick")
		self.password = self.config.get("nickserv", "password")
