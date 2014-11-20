import time
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
		self.name = "Tick Event"
		
class StartEvent(Event):
	def __init__(self):
		self.name = "Start Event"
		
class RunningEvent(Event):
	def __init__(self, host):
		self.name = "Running Event"
		self.host = host

class QuitEvent(Event):
	def __init__(self):
		self.name = "Quit Event"
		
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
	def __init__(self, message):
		self.name = "PING Event"
		self.message = message
		
class OutputEvent(Event):
	silent=True
	def __init__(self, origin, text):
		self.name = "Output Event"
		y, m, d, h, m, s, wd, yd, isdst = time.localtime()
		self.text = "%02d:%02d:%02d %s: %s" % (h, m, s, origin.upper(), text)
		
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
	def __init__(self, type):
		self.name = "Connection closed Event"
		self.type = type

class ReconnectEvent(Event):
	def __init__(self, message, master = ""):
		self.name = "Reconnect Event"
		self.message = message
		self.master = master

class ListenerPrintEvent(Event):
	def __init__(self):
		self.name = "Listener Print Event"

class ParsedPrivmsgEvent(Event):
	def __init__(self, nick, source, channel, message, command, parameters):
		self.name = "ParsedPrivmsg Event"
		self.nick = nick
		self.source = source
		self.channel = channel
		self.message = message
		self.command = command
		self.parameters = parameters

		