import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import TickEvent, PingEvent, ReloadconfigEvent, ListenerPrintEvent
import ConfigParser, time
from weakboundmethod import WeakBoundMethod as Wbm

class autopinger():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self.lastPing = time.time()
		self._connections = [
			self.ed.add(TickEvent, Wbm(self.ping)),
			self.ed.add(ReloadconfigEvent, Wbm(self.reload_config)),
			self.ed.add(PingEvent, Wbm(self.reset))
		]

	def reset(self, event):
		self.lastPing = time.time()
		
	def ping(self, event):
		if time.time() - self.lastPing > self.timeout:
			self.ed.post(PingEvent("trail and error..."))
			
	def reload_config(self, event):
		if event.module == "autopinger" or event.module == "all":
			self.read_config()
	
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.timeout = self.config.getint("autopinger", "timeout") + 2
