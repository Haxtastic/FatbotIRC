import thread
import socket, ssl
from networkview import NetworkView
from networkcontroller import NetworkController
from networkmessage import NetworkMessage
from events import *

class Connection:

	CLOSE_STATE_NONE = 0
	CLOSE_STATE_REQUESTED = 1
	CLOSE_STATE_CLOSING = 2
	
	def __init__(self, host, port, evManager):
		self.host = host
		self.port = port
		self.pendingRead = self.pendingWrite = 0
		self.readingError = self.writingError = False
		self.closeState = Connection.CLOSE_STATE_NONE
		self.socketClosed = False
		self.dead = False
		self.msg = NetworkMessage()
		self.evManager = evManager
		self.netview = NetworkView(self, self.evManager)
		self.netcontrol = NetworkController(self.evManager)
		self.connectionLock = thread.allocate_lock()
		self.ssl = None
		
	def connect(self, use_ssl=False):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if use_ssl:
			self.ssl = ssl.wrap_socket(self.socket)
			self.ssl.connect((self.host, self.port))
		else:
			self.socket.connect((self.host, self.port))
		self.pendingRead+=1
		thread.start_new_thread(self.parse_header, ())
		self.evManager.post(ConnectedEvent())
		return
	
	def parse_header(self):
		if self.closeState is Connection.CLOSE_STATE_CLOSING:
			if not self.closingConnection():
				self.connectionLock.release()
			return
			
		self.msg.buffer = self.safe_recv(2048)	#ACQUIRE PACKET BRO
		self.connectionLock.acquire()			#ACQUIRE LOCK
		self.pendingRead=-1
		thread.start_new_thread(self.parse_packet, ())
		self.connectionLock.release()
		
	def parse_packet(self):
		self.connectionLock.acquire()
		if self.closeState is Connection.CLOSE_STATE_CLOSING:
			if not closingConnection():
				self.connectionLock.release()
			return
		
		if self.netcontrol and self.msg.buffer != "":
			self.netcontrol.on_recv_message(self.msg)
		#else:
			#self.evManager.post(ConsoleEvent("Warning: [Connection::parse_packet] self.msg.buffer is empty."))
			
		self.msg.reset()
		#new thread
		self.pendingRead+=1
		thread.start_new_thread(self.parse_header, ())
		self.connectionLock.release()
		return
		
	def send(self, msg):
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
		#self.connectionLock.acquire()
		if self.closeState is not Connection.CLOSE_STATE_NONE:
			return
		self.closeState = Connection.CLOSE_STATE_REQUESTED
		thread.start_new_thread(self.close_connection_task, ())
		#self.connectionLock.release()
		return
		
	def close_connection_task(self):
		self.connectionLock.acquire()
		if self.closeState is not Connection.CLOSE_STATE_REQUESTED:
			self.evManager.post(ConsoleEvent("Error: [Connection::close_connection_task] closeState = " + str(self.closeState)))
			self.connectionLock.release()
			return
		self.closeState = Connection.CLOSE_STATE_CLOSING
		if not self.closing_connection():
			self.connectionLock.release()
		
	def closing_connection(self):
		if self.pendingWrite is 0 or self.writingError is True:
			if not self.socketClosed:
				if self.ssl:
					self.ssl.close()
				else:
					self.socket.close()
				self.socketClosed = True
		
			if self.pendingRead is 0:
				self.connectionLock.release()
				self.dead = True
				print "disconnected"
				return True
		return False
			
	def safe_send(self, msg):
		size = len(msg.buffer)
		#print msg.buffer
		#print size
		if size > 2048:
			size = 2048
		position = 0
		tries = 0
		while position is not size:
			if self.ssl:
				sent = self.ssl.write(msg.buffer[position:size])
			else:
				sent = self.socket.send(msg.buffer[position:size])
			position+=sent
			#print position
			
	def safe_recv(self, size):
		try:
			if self.ssl:
				return self.ssl.read(size)
			else:
				return self.socket.recv(size)
		except socket.error, msg:
			self.close_connection()
			self.post(ConsoleEvent("Connection closed"))
		return False
			