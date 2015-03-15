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
import time
"""
The events file.
These are all the events that the bot can send out.
"""

class Event:
	silent = False
	def __init__(self):
		self.name = "GENERIC Event"
		
	def post(self, ed):
		ed.post(self)
		
class LoginEvent(Event):
	def __init__(self, username):
		self.name = "LOGIN Event"
		self.description = "Sending user/nickname."
		self.username = username
		
# REQUEST DONE EVENTS

class JoinEvent(Event):
	def __init__(self, source, dest, master = ""):
		self.name = "JOIN event"
		self.source = source
		self.type = "JOIN"
		self.dest = dest
		self.master = master
		
class PartEvent(Event):
	def __init__(self, source, dest, master = ""):
		self.name = "PART event"
		self.source = source
		self.type = "PART"
		self.dest = dest
		self.master = master
		
class SendCommandEvent(Event):
	def __init__(self, type, data, master = ""):
		self.name = "SEND COMMAND Event"
		self.type = type
		self.data = data
		self.master = master

class SendPrivmsgEvent(Event):
	def __init__(self, source, dest, data, master = ""):
		self.name = "SEND PRIVMSG Event"
		self.source = source
		self.dest = dest
		self.data = data
		self.master = master
		
class PongEvent(Event):
	silent = True
	def __init__(self, data):
		self.name = "PONG Event"
		self.data = data
		
class DisconnectEvent(Event):
	def __init__(self, message, master = ""):
		self.name = "DISCONNECT Event"
		self.message = message
		self.master = master
		
class ReconnectEvent(Event):
	def __init__(self, message, master = ""):
		self.name = "RECONNECT Event"
		self.message = message
		self.master = master

# REQUEST EVENTS
		
class RequestJoinEvent(Event):
	def __init__(self, channel, master = ""):
		self.name = "REQUEST JOIN event"
		self.channel = channel
		self.master = master
		
class RequestPartEvent(Event):
	def __init__(self, channel, master = ""):
		self.name = "REQUEST PART event"
		self.channel = channel
		self.master = master

class RequestSendPrivmsgEvent(Event):
	def __init__(self, dest, message, master = ""):
		self.name = "REQUEST SEND PRIVMSG Event"
		self.dest = dest
		self.message = message
		self.master = master
		
class RequestSendCommandEvent(Event):
	def __init__(self, type, message, master = ""):
		self.name = "REQUEST SEND COMMAND Event"
		self.type = type
		self.message = message
		self.master = master
		
class RequestPongEvent(Event):
	silent = True
	def __init__(self, message):
		self.name = "REQUEST PONG Event"
		self.message = message
		
class RequestReconnectEvent(Event):
	def __init__(self, message, master = ""):
		self.name = "REQUEST RECONNECT Event"
		self.message = message
		self.master = master
		
class RequestDisconnectEvent(Event):
	def __init__(self, message, master = ""):
		self.name = "REQUEST DISCONNECT Event"
		self.message = message
		self.master = master

# SERVER EVENTS		
		
class JoinedEvent(Event):
	def __init__(self, source, type, dest, data):
		self.name = "JOINED Event"
		self.source = source
		self.type = type
		self.dest = dest
		self.data = data
		
class PartedEvent(Event):
	def __init__(self, source, type, dest, data):
		self.name = "PARTED Event"
		self.source = source
		self.type = type
		self.dest = dest
		self.data = data
		
class HosthiddenEvent(Event):
	def __init__(self, source, dest, data):
		self.name = "HOSTHIDDEN Event"
		self.source = source
		self.dest = dest
		self.data = data
		
class NoexistEvent(Event):
	def __init__(self, source, dest, data):
		self.name = "NOEXIST Event"
		self.source = source
		self.dest = dest
		self.data = data
		
class ModeEvent(Event):
	def __init__(self, source, type, dest, data):
		self.name = "MODE Event"
		self.source = source
		self.type = type
		self.dest = dest
		self.data = data
		
class ReginfoEvent(Event):
	def __init__(self, source, type, dest, data):
		self.name = "REGINFO Event"
		self.source = source
		self.type = type
		self.dest = dest
		self.data = data
		
class PrivmsgEvent(Event):
	def __init__(self, source, dest, data):
		self.name = "PRIVMSG Event"
		self.source = source
		self.dest = dest
		self.data = data
		
class NoticeEvent(Event):
	def __init__(self, source, type, dest, data):
		self.name = "NOTICE Event"
		self.source = source
		self.type = type
		self.dest = dest
		self.data = data

class ParsedPrivmsgEvent(Event):
	def __init__(self, nick, source, channel, message, command, parameters):
		self.name = "PARSEDPRIVMSG Event"
		self.nick = nick
		self.source = source
		self.channel = channel
		self.message = message
		self.command = command
		self.parameters = parameters
		
# INTERNAL EVENTS
		
class OutputEvent(Event):
	silent=True
	def __init__(self, origin, text):
		self.name = "OUTPUT Event"
		y, m, d, h, m, s, wd, yd, isdst = time.localtime()
		self.text = "[%02d:%02d:%02d] %s: %s" % (h, m, s, origin.upper(), text)

class TickEvent(Event):
	silent = True
	def __init__(self):
		self.name = "TICK Event"
		
class StartEvent(Event):
	def __init__(self):
		self.name = "START Event"

class QuitEvent(Event):
	def __init__(self):
		self.name = "QUIT Event"
		
class ConnectedEvent(Event):
	def __init__(self):
		self.name = "CONNECTED Event"
		self.description = "Connected to server."
		
class ReloadEvent(Event):
	def __init__(self):
		self.name = "RELOAD Event"		
		
class ReloadconfigEvent(Event):
	def __init__(self, module, master = ""):
		self.name = "RELOADCONFIG Event"
		self.module = module.lower()
		self.master = master
		
class WelcomeEvent(Event):
	def __init__(self, message):
		self.name = "WELCOME Event"
		self.message = message
		self.description = "Successfully logged in to server."

class OperEvent(Event):
	def __init__(self, message):
		self.name = "OPER Event"
		self.message = message
		
class PerformEvent(Event):
	def __init__(self, message):
		self.name = "PERFORM Event"
		self.message = message
		
class ConnectionClosedEvent(Event):
	def __init__(self, type):
		self.name = "CONNECTION CLOSED Event"
		self.type = type

		