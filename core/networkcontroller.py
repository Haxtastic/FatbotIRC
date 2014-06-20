from events import PingEvent, ConsoleEvent, WelcomeEvent, OperEvent, PerformEvent, PrivmsgEvent
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
		if msg.buffer != "":
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
			self.ed.post(PingEvent())
			return
		elif parameters[0] == "ERROR":
			self.ed.post(ConsoleEvent(buffer.strip()))
			return
		self.ed.post(ConsoleEvent(buffer.strip())) # Print message
		if len(parameters) < 2: # Two is too few parameters hurrhurr
			try:
				error = "Error: [NetworkController::parse_packet] parameters[0] = %s" % parameters[0]
			except TypeError:
				error = "Error: [NetworkController::parse_packet] TypeError when formatting parameters string"
			self.ed.post(ConsoleEvent(error))
		#Welcome message
		elif parameters[1] == "001":  # message
			self.ed.post(WelcomeEvent(parameters[3]))
		#Auth successful message
		elif parameters[1] == "900":  # message
			self.ed.post(OperEvent(parameters[3]))
		#Oper successful message
		elif parameters[1] == "381":  # message
			self.ed.post(PerformEvent(parameters[3]))
		#PRIVMSG
		elif parameters[1] == "PRIVMSG":  # Source	 channel 		message
			self.ed.post(PrivmsgEvent(parameters[0], parameters[2], parameters[3]))
			
		