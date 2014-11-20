import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import ReloadconfigEvent, SendPrivmsgEvent
from weakboundmethod import WeakBoundMethod as Wbm

class reloadconfigresponder():
	def __init__(self, ed):
		self.ed = ed
		self._connections = [
			self.ed.add(ReloadconfigEvent, Wbm(self.config)),
			self.ed.add(WelcomeEvent, Wbm(self.module))
		]
	
	def config(self, event):
		if event.module == "modules":
			return	
		self.ed.post(SendPrivmsgEvent(event.master, "Configurations reloaded, master!"))
		
	def module(self, event):
		if event.message != "modulereload":
			return
		self.ed.post(SendPrivmsgEvent(event.master, "Modules reloaded, master!"))
