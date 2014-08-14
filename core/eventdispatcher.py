from events import ConsoleEvent, TickEvent, ListenerPrintEvent, PrivmsgEvent
import thread, time
from weakboundmethod import WeakBoundMethod as Wbm

class Connection:
	"""
	This class is used make it easier for the listeners to remove themselves from the dictionary.
	The classes that add a method to the EventDispatcher get a connection object returned.
	This class knows which event class it is and which listener it is, for easy removal of the listener.
	It does this in the __del__ method so as soon as a connection object becomes obsolete it will disappear from the dispatchers list.
	"""
	def __init__(self, eventcls, listener, ed):
		self.eventcls = eventcls
		self.listener = listener
		self.ed = ed
	
	def __del__(self):
		self.ed._listeners[self.eventcls].remove(self.listener)
	
class EventDispatcher:
	"""
	This is our EventDispatcher, it sends out events to the listeners who are interested in them.
	It stores listeners as a dictionary with the event class as key and a list of methods from other classes as value.
	By doing this we only send events out to the classes who actually are interested in them.
	We have two event queues, since we do not want our program to halt every time someone posts a event.
	"""
	def __init__(self):
		self._listeners = dict()
		self.eventQueue = []
		self.nextQueue = []
		self.postLock = thread.allocate_lock()
		self.tickFreq = 0.5
		self.lastTick = time.time()
	
	def add(self, eventcls, listener):
		self._listeners.setdefault(eventcls, list()).append(listener)
		return Connection(eventcls, listener, self)
	
	def post(self, event): # Adds a event to the event queue, if the event isn't silent, then print it. Can be called from any thread.
		self.postLock.acquire()
		self.nextQueue.append(event)
		if not event.silent:
			self.nextQueue.append(ConsoleEvent(event.name))
		self.postLock.release()
	
	def consume_event_queue(self): # Actually dispatch the events
		self.postLock.acquire()
		self.eventQueue = self.nextQueue
		self.nextQueue = []
		self.postLock.release()
		if(time.time() - self.lastTick > self.tickFreq):
			self.eventQueue.append(TickEvent())
			self.lastTick = time.time()
		for event in self.eventQueue:
			try:
				for listener in self._listeners[event.__class__]:
					listener(event)
					#else:
					#	thread.start_new_thread(listener, (event, ))
			except KeyError:
				pass # No listener interested in this event

		
