#! /usr/bin/env python
from weakboundmethod import WeakBoundMethod as Wbm
from events import TickEvent, QuitEvent, StartEvent
from bot import Bot
import time

"""
This is our spinner class, it's what keeps the bot alive.
It will run until a QuitEvent has been sent out.
It consumes the event dispatchers queue and then sleeps for 0.01 seconds to reduce overhead.
"""

class Spinner:
	def __init__(self, ed):
		self.ed 		= ed
		self.alive 		= True
		self.event 		= TickEvent()
		self.bot 		= Bot(ed)
		self._connection = [
			self.ed.add(QuitEvent, Wbm(self.quit))
		]
		
	
	def run(self):
		self.ed.post(StartEvent())
		while self.alive is True:
			self.ed.consume_event_queue()
			time.sleep(0.01)
		
	def quit(self):
		self.alive = False
		