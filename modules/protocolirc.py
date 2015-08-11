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
from core.events import ParsedPrivmsgEvent, ReloadconfigEvent, RequestJoinEvent, RequestPartEvent, RequestSendPrivmsgEvent, ReloadconfigEvent, RequestDisconnectEvent, RequestReconnectEvent, RequestSendCommandEvent 
from core.botinfo import read_config_section
import ConfigParser
from core.weakboundmethod import WeakBoundMethod as Wbm

class protocolirc():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self._connections = [
			self.ed.add(ParsedPrivmsgEvent, Wbm(self.parse_privmsg)),
			self.ed.add(ReloadconfigEvent, Wbm(self.reload_config))
		]
		
	def parse_privmsg(self, event):
		nick, source = event.nick, event.source
		channel, message = event.channel, event.message
		command, parameters = event.command, event.parameters
		
		# :Kek!Keke@somekind.ofspecial.mask PRIVMSG Fatbot :Hey
		if (channel[0] == "#" and command != "fatbot") or " " not in message or not self.is_master(source):  # If no parameters or not master, discard
			return
		
		if command == "fatbot" and len(parameters) > 1:
			command = parameters[0]
			parameters = parameters[1:]
		
		if command == "join":  # channel
			#self.ed.post(JoinEvent(parameters[0], nick))
			RequestJoinEvent(parameters[0], nick).post(self.ed)
		elif command == "part":  # channel
			#self.ed.post(PartEvent(parameters[0], nick))
			RequestPartEvent(parameters[0], nick).post(self.ed)
		elif command == "send":  # destination, message
			text = ""
			for word in parameters[1:]:
				text += "%s " % (word, )
			#self.ed.post(SendPrivmsgEvent(parameters[0], text.strip(), nick))
			RequestSendPrivmsgEvent(parameters[0], text.strip(), nick).post(self.ed)
		elif command == "reloadconfig":  # list of modules to reload
			for module in parameters:
				#self.ed.post(ReloadconfigEvent(module, nick))
				ReloadconfigEvent(module, nick).post(self.ed)
		elif command == "disconnect" or command == "reconnect":
			text = ""
			for word in parameters:
				text += "%s " % (word, )
			text = text.strip()
			if command == "disconnect":
				#self.ed.post(DisconnectEvent(text, nick))
				RequestDisconnectEvent(text, nick).post(self.ed)
			elif command == "reconnect":
				#self.ed.post(ReconnectEvent(text, nick))
				RequestReconnectEvent(text, nick).post(self.ed)
			return
		elif command == "command":
			#self.ed.post(SendCommandEvent(parameters[0], parameters[1:]))
			RequestSendCommandEvent(parameters[0], parameters[1:]).post(self.ed)
		elif command == "execute":
			exec(" ".join(parameters))
			
	def reload_config(self, event):
		if event.module == "protocolirc" or event.module == "all":
			self.read_config()

	def is_master(self, source): # checks if source is master
		for master in self.masters:
			if source.lower() == master.lower():
				return True
		return False
			
	def read_config(self):
		config = read_config_section(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'), "protocolirc")
		#self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.masters = config["masters"]
			