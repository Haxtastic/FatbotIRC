from events import *
import thread

class EventManager:
	def __init__(self):
		from weakref import WeakKeyDictionary
		self.listeners = WeakKeyDictionary()
		self.eventQueue = []
		self.nextQueue = []
		self.listenersToAdd = []
		self.listenersToRemove = []
		self.postLock = thread.allocate_lock()
	
	def register_listener(self, listener):
		self.listenersToAdd.append(listener)
	
	def update_listeners(self):
		for listener in self.listenersToAdd:
			self.listeners[listener] = 1
		for listener in self.listenersToRemove:
			if listener in self.listeners:
				del self.listeners[listener]
	
	def unregister_listener(self, listener):
		self.listenersToRemove.append(listener)
	
	def post(self, event):
		self.eventQueue.append(event)
		if isinstance(event, TickEvent):
			self.update_listeners()
			self.consume_event_queue()
		else:
			if not event.silent:
				#print "event add to console"
				self.post(ConsoleEvent(event.name))
				
	def post_next(self, event):
		self.nextQueue.append(event)
		if not event.silent:
				print("Next", event.name)
	
	def consume_event_queue(self):
		i = 0
		while i < len(self.eventQueue):
			event = self.eventQueue[i]
			for listener in self.listeners.keys():
				thread.start_new_thread(listener.notify, (event, ))
			i += 1
			if self.listenersToAdd or self.listenersToRemove:
				self.update_listeners()
		self.eventQueue = self.nextQueue
		self.nextQueue = []