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
from events import PingEvent, OutputEvent, WelcomeEvent, OperEvent, PerformEvent, PrivmsgEvent, SendCommandEvent, ConnectionClosedEvent
from networkmessage import NetworkMessage

class NetworkController():
	"""
	This class is used too parse the input we get from the network at the lowest level, it only handles basic IRC protocol.
	It splits the input at line breaks since that means end of packet in the IRC protocol.
	It then parses these packets into the standard IRC packet form of [source, command, data] and posts the parameters with the right event.

	Note: In case of the packet being a ping or error, the first parameter is the command.
	"""
	def __init__(self, ed):
		self.ed = ed
		
	def on_recv_message(self, msg):
		msg.strip_message()
		messages = msg.buffer.split("\n")
		for text in messages:
			self.parse_packet(text)
		
	def parse_packet(self, buffer):
		#source, command, data
		parameters = buffer.split(" ", 3)
		if parameters[0].find(":") != -1:
			parameters[0] = parameters[0].split(":")[1]  # Get rid of the : at the start of the message
		if parameters[0] == "PING":
			parameters[1] = parameters[1].split(":")[1]
			self.ed.post(PingEvent(parameters[1]))
			return
		elif parameters[0] == "ERROR":
			self.ed.post(OutputEvent("Internal", buffer.strip()))
			self.ed.post(ConnectionClosedEvent("server"))
			return
		self.ed.post(OutputEvent("Server", buffer.strip())) # Print message
		if len(parameters) < 2: # Two is too few parameters hurrhurr
			try:
				if len(parameters) == 2:
					error = "Error: [NetworkController::parse_packet] parameters[0] = %s parameters[1] = %s" % (parameters[0], parameters[1])
				else:
					error = "Error: [NetworkController::parse_packet] parameters[0] = %s" % parameters[0]
			except TypeError:
				error = "Error: [NetworkController::parse_packet] TypeError when formatting parameters string"
			self.ed.post(OutputEvent("Internal", error))
		elif len(parameters) > 3 and parameters[1] == "NOTICE":
			if parameters[3].find("You are now logged in as") != -1:
				name = parameters[3].split(":You are now logged in as")[1].split(".")[0].strip()
				self.ed.post(SendCommandEvent("MODE", "%s +x" % name, ""))
		#Welcome message
		elif parameters[1] == "001":  # message
			self.ed.post(WelcomeEvent(parameters[3]))
		#Mask Hostname successful:
		elif parameters[1] == "396":
			self.ed.post(PerformEvent(parameters[3]))
		#Auth successful message
		elif parameters[1] == "900":  # message
			self.ed.post(OperEvent(parameters[3]))
		#Oper successful message
		elif parameters[1] == "381":  # message
			self.ed.post(PerformEvent(parameters[3]))
		#PRIVMSG
		elif parameters[1] == "PRIVMSG":  # Source	 channel 		message
			self.ed.post(PrivmsgEvent(parameters[0], parameters[2], parameters[3]))
			
		
