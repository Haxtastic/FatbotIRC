#! /usr/bin/env python
from events import TickEvent, QuitEvent
import time

class CPUSpinnerController:

	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.keepGoing = True
		
	
	def run(self):
		while self.keepGoing:
			event = TickEvent()
			self.evManager.postLock.acquire()
			self.evManager.post(event)
			self.evManager.postLock.release()
			time.sleep(0.001)


	def notify(self, event):
		if isinstance(event, QuitEvent):
			self.keepGoing = False
