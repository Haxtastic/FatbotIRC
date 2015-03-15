import os, sys
from core.events import *
import ConfigParser
from core.weakboundmethod import WeakBoundMethod as Wbm
from core.botinfo import read_config_section

class performer():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self._connections = [
			self.ed.add(NoticeEvent, Wbm(self.notice)),
			self.ed.add(HosthiddenEvent, Wbm(self.perform))
		]
		
	def notice(self, event):
		if "quakenet.org" in event.source.lower() or "are now logged in" not in event.data:
			return
		self.perform(event)
		
	def perform(self, event):
		for channel in self.channels:
			RequestJoinEvent(channel).post(self.ed)
			
	def read_config(self):
		config = read_config_section(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'), "performer")
		#self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.channels = config["channels"]
