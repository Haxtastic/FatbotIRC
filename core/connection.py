import thread, socket, ssl
from networkview import NetworkView
from networkcontroller import NetworkController
from networkmessage import NetworkMessage
from events import ConnectedEvent, ConsoleEvent, ConnectionClosedEvent
"""
Our connection class.
This class handles all the underlying data transfer between the bot and the server.
It has a send function which our Network viewer can call to send data to the server, it then sends it safely via it's internal methods.
It also handles all the data input from the server and makes sure that our network controller parses it.
"""

class Connection:

	CLOSE_STATE_NONE = 0
	CLOSE_STATE_REQUESTED = 1
	CLOSE_STATE_CLOSING = 2
	
	def __init__(self, host, port, ed):
		self.host = (host, port)
		self.pendingRead = self.pendingWrite = 0
		self.readingError = self.writingError = False
		self.closeState = Connection.CLOSE_STATE_NONE
		self.socketClosed = False
		self.dead = False
		self.msg = NetworkMessage()
		self.ed = ed
		self.netview = NetworkView(self, self.ed)
		self.netcontrol = NetworkController(self.ed)
		self.connectionLock = thread.allocate_lock()
		self.ssl = None
		
	def connect(self, use_ssl=False):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if use_ssl:
			self.ssl = ssl.wrap_socket(self.socket)
			self.ssl.connect(self.host)
		else:
			self.socket.connect(self.host)
		self.pendingRead+=1
		thread.start_new_thread(self.parse_header, ())
		self.ed.post(ConnectedEvent())
		return
	
	def parse_header(self):			
		if self.closeState is not Connection.CLOSE_STATE_NONE:
			#if not self.closingConnection():
			#self.connectionLock.release()
			return
		self.msg.buffer = self.safe_recv(2048)	#ACQUIRE PACKET BRO
		self.connectionLock.acquire()
		self.pendingRead=-1
		self.connectionLock.release()
		self.parse_packet()
		
	def parse_packet(self):
		self.netcontrol.on_recv_message(self.msg)
		self.msg.reset()
		#new thread
		self.connectionLock.acquire()
		self.pendingRead+=1
		thread.start_new_thread(self.parse_header, ())
		self.connectionLock.release()
		return
		
	def send(self, msg): # Can be called from any thread
		self.connectionLock.acquire()
		if self.closeState is Connection.CLOSE_STATE_CLOSING:
			#if not closingConnection():
			self.connectionLock.release()
			return False
		if self.pendingWrite is 0:
			self.netview.on_send_message(msg)
			self.internal_send(msg)
		else:
			pass
			
		self.connectionLock.release()
		return True
			
	def internal_send(self, msg):
		self.pendingWrite+=1
		self.safe_send(msg)
		self.on_write_operation(msg)
		
	def on_write_operation(self, msg):
		msg.reset()
		self.pendingWrite-=1
		
	def close_connection(self):
		self.connectionLock.acquire()
		if self.closeState is not Connection.CLOSE_STATE_NONE:
			self.connectionLock.release()
			return
		self.closeState = Connection.CLOSE_STATE_REQUESTED
		self.connectionLock.release()
		return self.close_connection_task()
		
	def close_connection_task(self):
		self.connectionLock.acquire()
		if self.closeState is not Connection.CLOSE_STATE_REQUESTED:
			self.ed.post(ConsoleEvent("Error: [Connection::close_connection_task] closeState = " + str(self.closeState)))
			self.connectionLock.release()
			return
		self.closeState = Connection.CLOSE_STATE_CLOSING
		if not self.closing_connection():
			self.connectionLock.release()
		
	def closing_connection(self):
		if self.pendingWrite is 0 or self.writingError is True:
			if not self.socketClosed:
				if self.ssl:
					self.ssl.shutdown(socket.SHUT_RDWR)
					self.ssl.close()
				else:
					self.socket.close()
				self.socketClosed = True
			if self.pendingRead is 0 or self.readingError is True:
				self.connectionLock.release()
				self.dead = True
				self.ed.post(ConnectionClosedEvent())
				return True
		return False
			
	def safe_send(self, msg):
		size = len(msg.buffer)
		if size > 2048:
			size = 2048
		position = 0
		while position is not size:
			try:
				if self.ssl:
					sent = self.ssl.write(msg.buffer[position:size])
				else:
					sent = self.socket.send(msg.buffer[position:size])
				position+=sent
			except socket.error, msg:
				self.writingError = True
			return position
				
	def safe_recv(self, size):
		try:
			if self.ssl:
				return self.ssl.read(size)
			else:
				return self.socket.recv(size)
		except socket.error, msg:
			self.readingError = True
		return False
			