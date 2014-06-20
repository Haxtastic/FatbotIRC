import thread
from events import TickEvent, ConsoleEvent
from weakboundmethod import WeakBoundMethod as Wbm
import time

"""
The console view class handles all output to the console.
It has a print queue and is thread safe to make sure every thing gets output in the right order.
"""

class ConsoleView:
	def __init__(self, ed):
		self.ed = ed
		self.printQueue = []
		self.queueLock = thread.allocate_lock()
		self._connection = [
			self.ed.add(TickEvent, Wbm(self.consume_queue)),
			self.ed.add(ConsoleEvent, Wbm(self.add))
		]
		
	def consume_queue(self, event):
		self.queueLock.acquire()
		for text in self.printQueue:
			print text
		self.printQueue = []
		self.queueLock.release()
		
	def add(self, event):
		self.queueLock.acquire()
		y, m, d, h, m, s, wd, yd, isdst = time.localtime()
		self.printQueue.append("%02d:%02d:%02d %s" % (h, m, s, event.text))
		self.queueLock.release()