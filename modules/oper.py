import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser
from weakboundmethod import WeakBoundMethod as Wbm

class oper():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self._connections = [
			self.ed.add(OperEvent, Wbm(self.identify))
		]
		
	def identify(self, event):
		self.ed.post(SendCommandEvent("OPER", "%s %s" % (self.nick, self.password), ""))
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.nick = self.config.get("oper", "nick")
		self.password = self.config.get("oper", "password")
