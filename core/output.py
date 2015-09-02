"""
Copyright 2014 Magnus Briden

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
		PrintEvent(output.text).post(self.ed)
		self.queueLock.release()
		
	
