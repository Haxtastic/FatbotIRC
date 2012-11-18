import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser, time

class autoPinger():
	def __init__(self, evManager):
		self.evManager = evManager
		self.read_config()
		self.lastPing = time.clock()
		self.evManager.register_listener(self)
		
	def notify(self, event):
		if isinstance(event, TickEvent):
			if abs(time.clock() - self.lastPing) > self.timeout:
				self.evManager.post(PingEvent())
		elif isinstance(event, PingEvent):
			self.lastPing = time.clock()
		elif isinstance(event, ReloadconfigEvent):
			if event.module == "autopinger" or event.module == "all":
				self.read_config()
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.timeout = self.config.getint("autopinger", "timeout") + 2
			
class evManager():
	def post(self, event):
		print event.name
		
	def register_listener(self, list):
		print "REGISTERD"
		
def main():
	manager = evManager()
	ping = autoPinger(manager)
	ping.notify(TickEvent())
	ping.notify(PingEvent())
	ping.notify(TickEvent())
	
if __name__ == '__main__':
	main()