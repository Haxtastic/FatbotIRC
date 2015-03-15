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
# encoding: UTF-8
import os, sys
from core.events import *
import ConfigParser
from core.weakboundmethod import WeakBoundMethod as Wbm
from core.botinfo import read_config_section

class nickserv():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self._connections = [
			self.ed.add(ReginfoEvent, Wbm(self.identify)),
			self.ed.add(NoticeEvent, Wbm(self.hostmask))
		]
		
	def identify(self, event):
		if event.type != "001":
			return
		if "quakenet" in event.source:
			RequestSendPrivmsgEvent("Q@Cserve.quakenet.org", "auth %s %s" % (self.nick, self.password)).post(self.ed)
		elif "dream-irc" in event.source:
			RequestSendPrivmsgEvent("nickserv", "identify %s" % (self.password, ), "").post(self.ed)
		else:
			RequestSendPrivmsgEvent("nickserv", "identify %s %s" % (self.nick, self.password), "").post(self.ed)
			
	def hostmask(self, event):
		if "are now logged in" not in event.data:
			return
		name = event.dest
		RequestSendCommandEvent("MODE", "%s +x" % name, "").post(self.ed)
			
	def read_config(self):
		config = read_config_section(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'), "nickserv")
		self.nick = config["nick"]
		self.password = config["password"]
