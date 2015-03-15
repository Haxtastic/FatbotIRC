import os, sys
from core.events import ReloadconfigEvent, RequestSendPrivmsgEvent, ReginfoEvent
from core.weakboundmethod import WeakBoundMethod as Wbm

class responder():
	def __init__(self, ed):
		self.ed = ed
		self._connections = [
			self.ed.add(ReloadconfigEvent, Wbm(self.config)),
			self.ed.add(ReginfoEvent, Wbm(self.module))
		]
	
	def config(self, event):
		if event.module == "modules":
			return
			RequestSendPrivmsgEvent(event.master, "Configurations reloaded, master!").post(self.ed)
		
	def module(self, event):
		pass
		#if event.message != "modulereload":
		#	return
		#self.ed.post(SendPrivmsgEvent(event.master, "Modules reloaded, master!"))
