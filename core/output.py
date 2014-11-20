class OutputView:
	"""
	The output view class handles all output, .
	It has a event queue and is thread safe to make sure every thing gets output in the right order.
	"""
	def __init__(self, ed):
		self.ed = ed
		self.outputQueue = []
		self.queueLock = thread.allocate_lock()
		self.origins = ["server", "bot", "internal"]
		self._connection = [
			self.ed.add(OutputEvent, Wbm(self.process))
		]
		
	def process(self, output):
		self.queueLock.acquire()
		y, m, d, h, m, s, wd, yd, isdst = time.localtime()
		text = "%02d:%02d:%02d %s: %s" % (h, m, s, output.origin.upper(), output.text)
		self.ed.post(PrintEvent(output.text)
		self.queueLock.release()
		
	
