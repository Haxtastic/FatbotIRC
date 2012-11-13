import struct

class NetworkMessage:
	def __init__(self):
		self.reset()
		return
		
	def reset(self):
		self.buffer = ""
		
	def end_message(self):
		self.buffer+="\n"
		
	def strip_message(self):
		self.buffer = self.buffer.strip('\n\r')