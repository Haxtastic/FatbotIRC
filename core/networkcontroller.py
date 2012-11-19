from events import *
from networkmessage import NetworkMessage
import time

class NetworkController():
	def __init__(self, evManager):
		self.evManager = evManager
		#self.evManager.register_listener(self)
		
	def on_recv_message(self, msg):
		msg.strip_message()
		messages = msg.buffer.split("\n")
		for text in messages:
			self.parse_packet(text)
		
	def parse_packet(self, buffer):
		#source, command, body
		y, m, d, h, m, s, wd, yd, isdst = time.localtime()
		self.evManager.post(ConsoleEvent("%02d:%02d:%02d %s" % (h, m, s, buffer)))
		parameters = buffer.split(" ", 3)
		if parameters[0].find(":") != -1:
			parameters[0] = parameters[0].split(":")[1]  # Get rid of the : at the start of the message
		if parameters[0] == "PING":
			self.evManager.post(PingEvent())
			return
		elif parameters[0] == "ERROR":
			return
		if len(parameters) < 2:
			try:
				error = "Error: [NetworkController::parse_packet] parameters[0] = %s" % parameters[0]
			except TypeError:
				error = "Error: [NetworkController::parse_packet] TypeError when formating parameters string"
			self.evManager.post(ConsoleEvent(error))
		#Welcome message
		elif parameters[1] == "001":  # message
			self.evManager.post(WelcomeEvent(parameters[3]))
		elif parameters[1] == "PRIVMSG":  # Source, channel, message
			self.evManager.post(PrivmsgEvent(parameters[0], parameters[2], parameters[3]))

	#----------------------------------------------------------------------
	def notify(self, event):
		pass
		