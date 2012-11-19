import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser

class performer():
	def __init__(self, evManager):
		self.evManager = evManager
		self.read_config()
		self.evManager.register_listener(self)
		
	def perform(self):
		for channel in self.channels:
			self.evManager.post(JoinEvent(channel))
		
	def notify(self, event):
		if isinstance(event, WelcomeEvent):
			self.perform()
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.channels = self.config.get("performer", "channels").replace(" ", "").split(",")
