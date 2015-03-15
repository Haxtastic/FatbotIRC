"""
Copyright 2014 Magnus Bridén

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
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
