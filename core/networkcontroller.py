from events import *
from networkmessage import NetworkMessage

class NetworkController():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		
	def on_recv_message(self, msg):
		msg.strip_message()
		self.prase_packet(msg)
		return 0
		
	def prase_packet(self, recv):
		#source, command, body
		self.evManager.post(ConsoleEvent(recv.buffer))
		#print "recv.buffer"
		parameters = recv.buffer.split(" ", 3)
		if parameters[0].find(":") != -1:
			parameters[0] = parameters[0].split(":")[1]  # Get rid of the : at the start of the message
		if parameters[0] == "PING":
			self.evManager.post(PingEvent())
		elif parameters[0] == "ERROR":
			return
		elif parameters[1] == "PRIVMSG":  # Source, channel, message
			self.evManager.post(PrivmsgEvent(parameters[0], parameters[2], parameters[3]))
			
	def disconnect(self):
		#print "ProtocolGame.disconnect"
		if self.connection is not False:
			self.connection.close_connection()
			self.connection = False

	#----------------------------------------------------------------------
	def notify(self, event):
		pass
		