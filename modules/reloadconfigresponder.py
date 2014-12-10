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
import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import ReloadconfigEvent, SendPrivmsgEvent
from weakboundmethod import WeakBoundMethod as Wbm

class reloadconfigresponder():
	def __init__(self, ed):
		self.ed = ed
		self._connections = [
			self.ed.add(ReloadconfigEvent, Wbm(self.config)),
			self.ed.add(WelcomeEvent, Wbm(self.module))
		]
	
	def config(self, event):
		if event.module == "modules":
			return	
		self.ed.post(SendPrivmsgEvent(event.master, "Configurations reloaded, master!"))
		
	def module(self, event):
		if event.message != "modulereload":
			return
		self.ed.post(SendPrivmsgEvent(event.master, "Modules reloaded, master!"))
