#! /usr/bin/env python
from weakboundmethod import WeakBoundMethod as Wbm
from events import TickEvent, QuitEvent, StartEvent
from bot import Bot
from eventdispatcher import EventDispatcher
import time, wx

class Spinner():
	"""
	This is our spinner class, it's what keeps the bot alive.
	It will run until a QuitEvent has been sent out.
	It consumes the event dispatchers queue and then sleeps for 0.01 seconds to reduce overhead.
	"""
	def __init__(self, ed):
		self.ed 		= ed
		self.alive 		= True
		self.bot 		= Bot(ed)
		self._connection = [
			self.ed.add(QuitEvent, Wbm(self.quit))
		]
		
	
	def run(self):
		self.bot.start()
		while self.alive is True:
			self.ed.consume_event_queue()
			time.sleep(0.1)
		
	def quit(self, event):
		self.alive = False
		
def main():
	Spinner(EventDispatcher()).run()

if __name__ == '__main__':
	main()
		
