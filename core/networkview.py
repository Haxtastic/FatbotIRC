from events import *
from networkmessage import NetworkMessage

class NetworkView():

	#----------------------------------------------------------------------
	def __init__(self, connection, evManager):
		self.connection = connection
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.msg = NetworkMessage()
		
	def on_send_message(self, msg):
		if msg.silent is False:
			self.evManager.post(ConsoleEvent(msg.buffer))
		msg.end_message()
		return 0
		
	def connect(self, username):
		self.msg.buffer = "USER " + username + " * 8 :" + username + " sloffson"
		self.connection.send(self.msg)
		self.msg.buffer = "NICK " + username
		self.connection.send(self.msg)
		
	def join_channel(self, channel):
		if channel.find("#") == -1:
			channel = "#" + channel
		self.msg.buffer = "JOIN " + channel
		self.connection.send(self.msg)
		
	def send_message(self, dest, message):
		self.msg.buffer = "PRIVMSG %s :%s" % (dest, message)
		self.connection.send(self.msg)
		
	def ping(self):
		self.msg.buffer = "PONG :" + self.connection.host
		self.msg.silent = False
		self.connection.send(self.msg)

	#----------------------------------------------------------------------
	def notify(self, event):
		if isinstance(event, LoginEvent):
			self.connect(event.username)
		elif isinstance(event, PingEvent):
			self.ping()
		elif isinstance(event, JoinEvent):
			self.join_channel(event.channel)
		elif isinstance(event, SendPrivmsgEvent):
			self.send_message(event.dest, event.message)
