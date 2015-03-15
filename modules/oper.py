import os, sys
from core.events import *
import ConfigParser
from core.weakboundmethod import WeakBoundMethod as Wbm

class oper():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self._connections = [
			self.ed.add(OperEvent, Wbm(self.identify))
		]
		
	def identify(self, event):
		#self.ed.post(SendCommandEvent("OPER", "%s %s" % (self.nick, self.password), ""))
		SendCommandEvent("OPER", "%s %s" % (self.nick, self.password), "").post(self.ed)
			
	def read_config(self):
		config = read_config_section(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'), "oper")
		#self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.nick = config["nick"]
		self.password = config["password"]
