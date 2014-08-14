class NetworkMessage:
	"""
	A simple class to ease message output to the server.
	Basically just a wrapper for the output buffer.
	"""
	def __init__(self, netmsg=None):
		if(netmsg == None):
			self.buffer = ""
			self.reset()
			self.silent = False
		else:
			self.buffer = netmsg.buffer
			self.silent = netmsg.silent
		return
		
	def reset(self):
		self.buffer = ""
		
	def end_message(self):
		self.buffer+="\n"
		
	def strip_message(self):
		self.buffer = self.buffer.strip('\n\r')
