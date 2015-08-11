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
from events import NoticeEvent, ModeEvent, RequestPongEvent, OutputEvent, ReginfoEvent, OperEvent, PerformEvent, PrivmsgEvent, RequestSendCommandEvent, ConnectionClosedEvent, NoexistEvent, HosthiddenEvent, JoinedEvent, PartedEvent
from networkmessage import NetworkMessage
from weakboundmethod import WeakBoundMethod as Wbm

class NetworkController():
	"""
	This class is used too parse the input we get from the network at the lowest level, it only handles basic IRC protocol.
	It splits the input at line breaks since that means end of packet in the IRC protocol.
	It then parses these packets into the standard IRC packet form of [source, command, data] and posts the parameters with the right event.

	Note: In case of the packet being a ping or error, the first parameter is the command.
	"""
	def __init__(self, ed):
		self.ed = ed
		self.accumulator = ""
		self.parsers = {
			"NOTICE"	: Wbm(self.parse_notice),
			"AUTH"		: Wbm(self.parse_notice),
			"001"		: Wbm(self.parse_reginfo),
			"002"		: Wbm(self.parse_reginfo),
			"003"		: Wbm(self.parse_reginfo),
			"004"		: Wbm(self.parse_reginfo),
			"005"		: Wbm(self.parse_reginfo),
			"396"		: Wbm(self.parse_hosthidden),
			"401"		: Wbm(self.parse_noexist),
			"PRIVMSG"	: Wbm(self.parse_privmsg),
			"MODE"		: Wbm(self.parse_mode),
			"JOIN"		: Wbm(self.parse_joined),
			"PART"		: Wbm(self.parse_parted)
		}
		
	def on_recv_message(self, msg):
		msg.buffer = self.accumulator + msg.buffer
		lines = msg.prepare_message()
		self.accumulator = "" if msg.buffer.endswith("\r\n") else lines.pop()
		for line in lines:
			self.parse_message(line.lstrip(":"))
			
	def parse_message(self, buffer):
		if buffer.count(" ") < 2:
			command, data = buffer.split(" ", 1)
			if command == "PING":
				return RequestPongEvent(data.lstrip(":")).post(self.ed)
			elif command == "ERROR":
				OutputEvent("Internal", buffer.strip()).post(self.ed)
				ConnectionClosedEvent("server").post(self.ed)
				return
			else:
				try:
					error = "Error: [NetworkController::parse_packet] command = %s data = %s" % (command, data)
				except TypeError:
					error = "Error: [NetworkController::parse_packet] TypeError when formatting parameters string"
				OutputEvent("Internal", error).post(self.ed)
			
		OutputEvent("Server", buffer.strip()).post(self.ed) # Print message
		
		if buffer.count(" ") < 3:
			source, type, dest = buffer.split(" ", 2)
			data = ""
		else:
			source, type, dest, data = buffer.split(" ", 3) # source, type, dest, data
		
		if type in self.parsers.keys():
			self.parsers[type](source, type, dest, data)
		
	def parse_notice(self, source, type, dest, data):
		NoticeEvent(source, type, dest, data).post(self.ed)
		
	def parse_reginfo(self, source, type, dest, data):
		ReginfoEvent(source, type, dest, data).post(self.ed)
	
	def parse_mode(self, source, type, dest, data):
		ModeEvent(source, type, dest, data).post(self.ed)
		
	def parse_privmsg(self, source, type, dest, data):
		PrivmsgEvent(source, dest, data).post(self.ed)
	
	def parse_noexist(self, source, type, dest, data):
		NoexistEvent(source, dest, data).post(self.ed)
		
	def parse_hosthidden(self, source, type, dest, data):
		HosthiddenEvent(source, dest, data).post(self.ed)
	
	def parse_joined(self, source, type, dest, data):
		JoinedEvent(source, type, dest, data).post(self.ed)
	
	def parse_parted(self, source, type, dest, data):
		PartedEvent(source, type, dest, data).post(self.ed)