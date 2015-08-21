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
# encoding: UTF-8
import os, sys
from core.events import *
import ConfigParser
from core.weakboundmethod import WeakBoundMethod as Wbm
import os, sys
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)
from botinfo import bot_info

class performer():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self._connections = [
			self.ed.add(NoticeEvent, Wbm(self.notice)),
			self.ed.add(HosthiddenEvent, Wbm(self.perform))
		]
		
	def notice(self, event):
		if "quakenet.org" in event.source.lower() or "are now logged in" not in event.data:
			return
		self.perform(event)
		
	def perform(self, event):
		for channel in self.channels:
			RequestJoinEvent(channel).post(self.ed)
			
	def read_config(self):
		#config = read_config_section(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'), "performer")
		config 				= bot_info["performer"];
		#self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.channels = config["channels"]
