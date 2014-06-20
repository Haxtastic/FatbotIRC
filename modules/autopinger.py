import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import PingEvent, ReloadconfigEvent
import ConfigParser, time
from weakboundmethod import WeakBoundMethod as Wbm

class autopinger():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self.lastPing = time.clock()
		self._connections = [
			self.ed.add(PingEvent, Wbm(self.ping)),
			self.ed.add(ReloadconfigEvent, Wbm(self.reload_config))
		]
		
	def ping(self, event):
		if abs(time.clock() - self.lastPing) > self.timeout:
			self.ed.post(PingEvent())
			self.lastPing = time.clock()
			
	def reload_config(self, event):
		if event.module == "autopinger" or event.module == "all":
			self.read_config()
	
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.timeout = self.config.getint("autopinger", "timeout") + 2
