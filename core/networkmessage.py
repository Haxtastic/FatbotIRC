"""
A simple class to ease message output to the server.
Basically just a wrapper for the output buffer.
"""
class NetworkMessage:
	def __init__(self):
		self.buffer = ""
		self.reset()
		self.silent = False
		return
		
	def reset(self):
		self.buffer = ""
		
	def end_message(self):
		self.buffer+="\n"
		
	def strip_message(self):
		self.buffer = self.buffer.strip('\n\r')