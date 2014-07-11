from events import LoginEvent, PingEvent, JoinEvent, PartEvent, SendPrivmsgEvent, SendCommandEvent, DisconnectEvent, ReconnectEvent, ConsoleEvent, QuitEvent
from networkmessage import NetworkMessage
from weakboundmethod import WeakBoundMethod as Wbm

class NetworkView():
	"""
	This is the class we use to handle all the output to the network.
	Events gets posted with their relevant parameters and this class handles them accordingly.
	All methods are pretty straight forward, they do as their named.

	These methods can be executed by either the bot itself or by a master ordering it to.
	"""
	def __init__(self, connection, ed):
		self.connection = connection
		self.ed = ed
		self.msg = NetworkMessage()
		self._connections = [
			self.ed.add(LoginEvent, Wbm(self.connect)),
			self.ed.add(PingEvent, Wbm(self.ping)),
			self.ed.add(JoinEvent, Wbm(self.join_channel)),
			self.ed.add(PartEvent, Wbm(self.part_channel)),
			self.ed.add(SendPrivmsgEvent, Wbm(self.send_message_event)),
			self.ed.add(SendCommandEvent, Wbm(self.send_command)),
			self.ed.add(DisconnectEvent, Wbm(self.disconnect)),
			self.ed.add(ReconnectEvent, Wbm(self.reconnect))
		]
		
	def send_message_event(self, event):
		self.send_message(event.dest, event.message, event.master)
		
	def on_send_message(self, msg): # Called by instance owner(connection) every time a message is sent
		if msg.silent is False:
			self.ed.post(ConsoleEvent(msg.buffer))
		msg.end_message()
		
	def connect(self, event):
		self.msg.buffer = "USER " + event.username + " * 8 :" + event.username + " sloffson"
		self.connection.send(self.msg)
		self.msg.buffer = "NICK " + event.username
		self.connection.send(self.msg)
		
	def join_channel(self, event):
		channel = self.make_channel(event.channel)
		self.msg.buffer = "JOIN " + channel
		self.connection.send(self.msg)
		if event.master != "":
			self.send_message(event.master, "Joining channel '%s', master!" % (channel), "")
		
	def part_channel(self, event):
		channel = self.make_channel(event.channel)
		self.msg.buffer = "PART " + channel
		self.connection.send(self.msg)
		if event.master != "":
			self.send_message(event.master, "Parting channel '%s', master!" % (channel), "")
		
	def send_command(self, event):
		self.msg.buffer = "%s %s" % (event.type, event.message)
		self.connection.send(self.msg)
		if event.master != "":
			self.send_message(event.master, "Command '%s' sent with parameters '%s', master!" % (event.type, event.message), "")
		
	def send_message(self, dest, message, master):
		self.msg.buffer = "PRIVMSG %s :%s" % (dest, message)
		print self.msg.buffer
		self.connection.send(self.msg)
		if master != "":
			self.send_message(master, "Message '%s' sent to '%s', master!" % (message, dest), "")
		
	def ping(self, event):
		self.msg.buffer = "PONG :" + self.connection.host[0]
		self.msg.silent = False
		self.connection.send(self.msg)
		
	def make_channel(self, channel):
		if channel[0] != "#":
			channel = "#" + channel
		return channel
		
	def disconnect(self, event):
		if self.connection is not False:
			if event.master != "":
				self.send_message(event.master, "Disconnecting with message '%s', master!" % (event.message), "")
			self.msg.buffer = "QUIT " + event.message
			self.connection.send(self.msg)
			self.connection.close_connection("user")
			self.connection = False

	def reconnect(self, event):
		if self.connection is not False:
			if event.master != "":
				self.send_message(event.master, "Reconnecting with message '%s', master!" % (event.message), "")
			self.msg.buffer = "QUIT " + event.message
			self.connection.send(self.msg)
			self.connection.close_connection("reconnect")
			self.connection = False
