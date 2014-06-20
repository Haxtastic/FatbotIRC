"""
The events file.
These are all the events that the bot can send out.
"""

class Event:
	silent = False
	def __init__(self):
		self.name = "Generic Event"
		
class TickEvent(Event):
	def __init__(self):
		self.name = "Tick"
		
class StartEvent(Event):
	def __init__(self):
		self.name = "Start up"
		
class RunningEvent(Event):
	def __init__(self):
		self.name = "Bot up and running"
		
class QuitEvent(Event):
	def __init__(self):
		self.name = "Program Quit"
		
class ConnectedEvent(Event):
	def __init__(self):
		self.name = "Connected"
		
class LoginEvent(Event):
	def __init__(self, username):
		self.name = "Login in"
		self.username = username
		
class PrivmsgEvent(Event):
	def __init__(self, source, channel, message):
		self.name = "PRIVMSG Event"
		self.source = source
		self.channel = channel
		self.message = message
		
class JoinEvent(Event):
	def __init__(self, channel, master = ""):
		self.name = "JOIN event"
		self.channel = channel
		self.master = master
		
class PartEvent(Event):
	def __init__(self, channel, master = ""):
		self.name = "PART event"
		self.channel = channel
		self.master = master

class SendPrivmsgEvent(Event):
	def __init__(self, dest, message, master = ""):
		self.name = "Send PRIVMSG Event"
		self.dest = dest
		self.message = message
		self.master = master
		
class SendCommandEvent(Event):
	def __init__(self, type, message, master = ""):
		self.name = "Send COMMAND Event"
		self.type = type
		self.message = message
		self.master = master
		
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
	def __init__(self, module, master = ""):
		self.name = "Reloadconfig Event"
		self.module = module.lower()
		self.master = master
		
class DisconnectEvent(Event):
	def __init__(self, message, master = ""):
		self.name = "Disconnect Event"
		self.message = message
		self.master = master
		
class WelcomeEvent(Event):
	def __init__(self, message):
		self.name = "Welcome Event"
		self.message = message

class OperEvent(Event):
	def __init__(self, message):
		self.name = "Oper Event"
		self.message = message
		
class PerformEvent(Event):
	def __init__(self, message):
		self.name = "Perform Event"
		self.message = message
		
class ConnectionClosedEvent(Event):
	def __init__(self):
		self.name = "Connection closed Event"