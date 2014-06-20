import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser
from weakboundmethod import WeakBoundMethod as Wbm

class performer():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self._connections = [
			self.ed.add(PerformEvent, Wbm(self.perform))
		]
		
	def perform(self, event):
		for channel in self.channels:
			self.ed.post(JoinEvent(channel))
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.channels = self.config.get("performer", "channels").replace(" ", "").split(",")
