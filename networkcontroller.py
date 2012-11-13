from events import *
from networkmessage import NetworkMessage

class NetworkController():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		
	def on_recv_message(self, msg):
		msg.strip_message()
		print msg.buffer
		self.prase_packet(msg)
		return 0
		
	def prase_packet(self, recv):
		#source, command, body
		parameters = recv.buffer.split(" ", 3)
		if parameters[0] == "PING":
			self.evManager.post(PingEvent())
			return
		if parameters[0] == "":
			return
		parameters[0] = parameters[0].split(":")[1]  # Get rid of the : at the start of the message
		#if parameters[0] != config.owner:  # If owner didn't send the message, discard
		#	return
		if parameters[1] == "PRIVMSG":  # Source, channel, message
			self.prase_privmsg(parameters[0], parameters[2], parameters[3])
			
	def prase_privmsg(self, source, channel, message):
		# :Kek!Keke@somekind.ofspecial.mask PRIVMSG Fatbot :Hey
		if message.find(" ") == -1:  # If no parameters, discard
			return
		command = message.split(" ", 1)
		parameters = command[1]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		self.evManager.post(PrivmsgEvent(source, channel, message, command, parameters))
			
	def disconnect(self):
		#print "ProtocolGame.disconnect"
		if self.connection is not False:
			self.connection.close_connection()
			self.connection = False

	#----------------------------------------------------------------------
	def notify(self, event):
		pass
		