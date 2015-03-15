"""
Copyright 2014 Magnus Bridén

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
class NetworkMessage:
	"""
	A simple class to ease message output to the server.
	Basically just a wrapper for the output buffer.
	"""
	def __init__(self, dc=False, dc_msg="", netmsg=None):
		if(netmsg == None):
			self.reset()
			self.silent = False
			self.dc_send = dc
			self.dc_msg = dc_msg
		else:
			self.buffer = netmsg.buffer
			self.silent = netmsg.silent
			self.dc_send = netmsg.dc_send
			self.dc_msg = netmsg.dc_msg
		return
		
	def reset(self):
		self.buffer = ""
		
	def end_message(self):
		self.buffer+='\n'
		self.buffer = self.buffer.encode("utf-8")
		
	def strip_message(self):
		self.buffer = self.buffer.replace('\r', '').strip('\n')
		
	def prepare_message(self):
		return filter(None, self.buffer.decode("utf-8").splitlines())#.replace('\r', '').strip('\n').split('\n')
