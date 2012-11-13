from events import *
from networkmessage import NetworkMessage

class Protocol:
	def __init__(self, connection):
		self.connection = connection
		
	def on_send_message(self, msg):
		print msg.buffer
		msg.end_message()
		return 0
		
	def on_recv_message(self, msg):
		msg.strip_message()
		print msg.buffer
		self.prase_packet(msg)
		return 0
		
	def prase_packet(self, msg):
		pass
		
	def release_protocol(self):
		pass
		#if self.connection is not False:
		#	self.connection.close_connection()
		#	self.connection = False
		
class ProtocolIRC(Protocol):
	def __init__(self, connection, evManager):
		Protocol.__init__(self, connection)
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.msg = NetworkMessage()
		
	def prase_packet(self, recv):
		#source, command, body
		parameters = recv.buffer.split(" ", 3)
		if parameters[0] == "PING":
			self.ping()
			return
		if parameters[0] == "":
			return
		parameters[0] = parameters[0].split(":")[1]  # Get rid of the : at the start of the message
		#if parameters[0] != config.owner:  # If owner didn't send the message, discard
		#	return
		if parameters[1] == "PRIVMSG":
			self.prase_privmsg(parameters[0], parameters[2], parameters[3])
		
	def connect(self, username):
		self.msg.buffer = "USER " + username + " * 8 :" + username+" sloffson"
		self.connection.send(self.msg)
		self.msg.buffer = "NICK " + username
		self.connection.send(self.msg)
		
	def disconnect(self):
		#print "ProtocolGame.disconnect"
		if self.connection is not False:
			self.connection.close_connection()
			self.connection = False
	
	def ping(self):
		self.msg.buffer = "PONG :" + self.connection.host
		self.connection.send(self.msg)
		
	def prase_privmsg(self, source, channel, message):
		#:Kek!Keke@somekind.ofspecial.mask PRIVMSG Fatbot :Hey
		if message.find(" ") == -1:  # If no parameters, discard
			return
		command = message.split(" ", 1)
		parameters = command[1]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		self.evManager.post(PrivmsgEvent(source, channel, message, command, parameters))
			
			
	def join_channel(self, channel):
		if channel.find("#") == -1:
			channel = "#" + channel
		self.msg.buffer = "JOIN " + channel
		self.connection.send(self.msg)
		
	def send_message(self, channel, message):
		self.msg.buffer = "PRIVMSG %s :%s" % (channel, message)
		self.connection.send(self.msg)
			
		
	def notify(self, event):
		if isinstance(event, ConnectedEvent):
			self.connect(event.username)
		elif isinstance(event, JoinEvent):
			self.join_channel(event.channel)
		elif isinstance(event, SendPrivmsgEvent):
			self.send_message(event.channel, event.message)
			
			
			
		
