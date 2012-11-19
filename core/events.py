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
	def __init__(self):
		self.name = "Connected Event"
		
class LoginEvent(Event):
	def __init__(self, username):
		self.name = "Login Event"
		self.username = username
		
class PrivmsgEvent(Event):
	def __init__(self, source, channel, message):
		self.name = "PRIVMSG Event"
		self.source = source
		self.channel = channel
		self.message = message
		
class JoinEvent(Event):
	def __init__(self, channel):
		self.name = "JOIN event"
		self.channel = channel
		
class PartEvent(Event):
	def __init__(self, channel):
		self.name = "PART event"
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
		
class ConsoleEvent(Event):
	silent = True
	def __init__(self, text):
		self.name = "Console Event"
		self.text = text
		
class ReloadconfigEvent(Event):
	def __init__(self, module):
		self.name = "Reloadconfig Event"
		self.module = module.lower()
		
class DisconnectEvent(Event):
	def __init__(self, message):
		self.name = "Disconnect Event"
		self.message = message
		
class WelcomeEvent(Event):
	def __init__(self, message):
		self.name = "Welcome Event"
		self.message = message
