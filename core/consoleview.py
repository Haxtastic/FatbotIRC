import thread
from events import *
import time

class ConsoleView:
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.printQueue = []
		self.queueLock = thread.allocate_lock()
		
	def consume_queue(self):
		self.queueLock.acquire()
		for text in self.printQueue:
			print text
		self.printQueue = []
		self.queueLock.release()
		
	def notify(self, event):
		if isinstance(event, ConsoleEvent):
			self.queueLock.acquire()
			y, m, d, h, m, s, wd, yd, isdst = time.localtime()
			self.printQueue.append("%02d:%02d:%02d %s" % (h, m, s, event.text))
			self.queueLock.release()
		elif isinstance(event, TickEvent):
			self.consume_queue()
		