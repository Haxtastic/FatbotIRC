import thread
from events import *

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
			self.printQueue.append(event.text)
			self.queueLock.release()
		elif isinstance(event, TickEvent):
			self.consume_queue()
		