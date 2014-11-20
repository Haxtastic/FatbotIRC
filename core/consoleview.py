import thread
from events import TickEvent, OutputEvent
from weakboundmethod import WeakBoundMethod as Wbm
import time

class ConsoleView:
	"""
	The console view class handles all output to the console.
	It has a print queue and is thread safe to make sure every thing gets output in the right order.
	"""
	def __init__(self, ed):
		self.ed = ed
		self.printQueue = []
		self.queueLock = thread.allocate_lock()
		self._connection = [
			self.ed.add(TickEvent, Wbm(self.consume_queue)),
			self.ed.add(OutputEvent, Wbm(self.add))
		]
		
	def consume_queue(self, event):
		self.queueLock.acquire()
		for text in self.printQueue:
			print text
		self.printQueue = []
		self.queueLock.release()
		
	def add(self, event):
		self.queueLock.acquire()
		self.printQueue.append(event.text)
		self.queueLock.release()
