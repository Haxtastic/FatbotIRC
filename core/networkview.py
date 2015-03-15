from events import RequestPongEvent, RequestJoinEvent, RequestPartEvent, RequestSendPrivmsgEvent, RequestSendCommandEvent, RequestDisconnectEvent, RequestReconnectEvent
from events import LoginEvent, PongEvent, JoinEvent, PartEvent, SendPrivmsgEvent, SendCommandEvent, DisconnectEvent, ReconnectEvent, OutputEvent, QuitEvent, TickEvent
from networkmessage import NetworkMessage
from weakboundmethod import WeakBoundMethod as Wbm
import thread, time

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
		#self.msg = NetworkMessage()
		self.send_queue = []
		self.send_lock = thread.allocate_lock()
		self.message_time = 0
		self.messages_sent = 0
		self.total_messages_sent = 0
		self.max_messages_per_second = 4
		self._connections = [
			self.ed.add(LoginEvent, Wbm(self.connect)),
			self.ed.add(RequestPongEvent, Wbm(self.pong)),
			self.ed.add(RequestJoinEvent, Wbm(self.join_channel)),
			self.ed.add(RequestPartEvent, Wbm(self.part_channel)),
			self.ed.add(RequestSendPrivmsgEvent, Wbm(self.send_message_event)),
			self.ed.add(RequestSendCommandEvent, Wbm(self.send_command)),
			self.ed.add(RequestDisconnectEvent, Wbm(self.disconnect)),
			self.ed.add(RequestReconnectEvent, Wbm(self.reconnect)),
			self.ed.add(TickEvent, Wbm(self.consume_send_pool))
		]
		
	def send_message_event(self, event):
		self.send_message(event.dest, event.message, event.master)
		
	def on_send_message(self, msg): # Called by instance owner(connection) every time a message is sent
		if msg.silent is False:
			#self.ed.post(OutputEvent("Bot", msg.buffer))
			OutputEvent("Bot", msg.buffer).post(self.ed)
		msg.end_message()
		
	def connect(self, event):
		msg = NetworkMessage()
		msg.buffer = "USER " + event.username + " * 8 :" + event.username + " sloffson"
		self.send(msg)
		msg = NetworkMessage()
		msg.buffer = "NICK " + event.username
		self.username = event.username
		self.send(msg)
		
	def join_channel(self, event):
		msg = NetworkMessage()
		channel = self.make_channel(event.channel)
		msg.buffer = "JOIN " + channel
		self.send(msg)
		if event.master != "":
			self.send_message(event.master, "Joining channel '%s', master!" % (channel), "")
		JoinEvent(self.username, channel, event.master).post(self.ed)
		
	def part_channel(self, event):
		msg = NetworkMessage()
		channel = self.make_channel(event.channel)
		msg.buffer = "PART " + channel
		self.send(msg)
		if event.master != "":
			self.send_message(event.master, "Parting channel '%s', master!" % (channel), "")
		PartEvent(self.username, channel, event.master).post(self.ed)
		
	def send_command(self, event):
		msg = NetworkMessage()
		msg.buffer = "%s " % event.type
		if not isinstance(event.message, basestring):
			for word in event.message:
				msg.buffer += "%s " % word
			msg.buffer = msg.buffer.strip()
		else:
			msg.buffer = "%s %s" % (msg.buffer, event.message)
		self.send(msg)
		if event.master != "":
			self.send_message(event.master, "Command '%s' sent with parameters '%s', master!" % (event.type, event.message), "")
		SendCommandEvent(event.type, event.message, event.master).post(self.ed)

	def send_message(self, dest, message, master):
		msg = NetworkMessage()
		msg.buffer = "PRIVMSG %s :%s" % (dest, message)
		self.send(msg)
		if master != "":
			self.send_message(master, "Message '%s' sent to '%s', master!" % (message, dest), "")
		SendPrivmsgEvent(self.username, dest, message, master).post(self.ed)
		
	def pong(self, event):
		msg = NetworkMessage()
		msg.buffer = "PONG :" + event.message
		msg.silent = True
		self.send(msg)
		PongEvent(event.message).post(self.ed)
		
	def make_channel(self, channel):
		if channel[0] != "#":
			channel = "#" + channel
		return channel
		
	def send(self, msg):
		self.send_lock.acquire()
		self.send_queue.append(msg)
		self.send_lock.release()
		
	def disconnect(self, event):
		msg = NetworkMessage(True, "user")
		if self.connection is not False:
			if event.master != "":
				self.send_message(event.master, "Disconnecting with message '%s', master!" % (event.message), "")
			msg.buffer = "QUIT :" + event.message
			self.send(msg)
			DisconnectEvent(event.message, event.master).post(self.ed)
			

	def reconnect(self, event):
		msg = NetworkMessage(True, "reconnect")
		if self.connection is not False:
			if event.master != "":
				self.send_message(event.master, "Reconnecting with message '%s', master!" % (event.message), "")
			msg.buffer = "QUIT " + event.message
			self.send(msg)
			ReconnectEvent(event.message, event.master).post(self.ed)
			
	def consume_send_pool(self, event):
		self.send_lock.acquire()
		if time.time() - self.message_time > (1000/self.max_messages_per_second):
			self.message_time = time.time()
			self.messages_sent = max(self.messages_sent-1, 0)
		
		if len(self.send_queue) <= 0 or not self.connection or self.messages_sent >= self.max_messages_per_second:
			self.send_lock.release()
			return
			
		msg = self.send_queue.pop(0)
		self.connection.send(msg)
		if msg.dc_send:
			self.connection.close_connection(msg.dc_msg)
			self.connection = False
			
		self.send_lock.release()
		
			
