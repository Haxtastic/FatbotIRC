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
#! /usr/bin/env python
from weakboundmethod import WeakBoundMethod as Wbm
from events import TickEvent, QuitEvent, StartEvent
from bot import Bot
import time, wx, botinfo, eventdispatcher

class Spinner():
	"""
	This is our spinner class, it's what keeps the bot alive.
	It will run until a QuitEvent has been sent out.
	It consumes the event dispatchers queue and then sleeps for 0.01 seconds to reduce overhead.
	"""
	def __init__(self):
		self.ed 		= botinfo.bot_info["ed"] = eventdispatcher.EventDispatcher()
		self.alive 		= True
		self.bot 		= Bot(self.ed)
		self._connection = [
			self.ed.add(QuitEvent, Wbm(self.quit))
		]
		self.bot.start()
		
	
	def tick(self):
		self.ed.consume_event_queue()
		return self.alive
		
	def quit(self, event):
		self.alive = False

def main():
	spin = Spinner()
	while spin.tick():
		time.sleep(0.01)
	
