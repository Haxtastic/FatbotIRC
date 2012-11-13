class Event:
	silent = False
	def __init__(self):
		self.name = "Generic Event"
		
class TickEvent(Event):
	def __init__(self):
		self.name = "Tick"
		
class QuitEvent(Event):
	def __init__(self):
		self.name = "Program Quit"
		
class ConnectedEvent(Event):
	def __init__(self, username):
		self.name = "Connected Event"
		self.username = username
		
class PrivmsgEvent(Event):
	def __init__(self, source, channel, message, command, parameters):
		self.name = "PRIVMSG Event"
		self.source = source
		self.channel = channel
		self.message = message
		self.command = command
		self.parameters = parameters
		
class JoinEvent(Event):
	def __init__(self, channel):
		self.name = "JOIN event"
		self.channel = channel

class SendPrivmsgEvent(Event):
	def __init__(self, dest, message):
		self.name = "Send PRIVMSG Event"
		self.dest = dest
		self.message = message
		
class PingEvent(Event):
	silent = True
	def __init__(self):
		self.name = "PING Event"
		
