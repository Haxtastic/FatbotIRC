import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser
import random

class GuessnumberManager():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.read_config()
		self.games = {}
		self.errormessage = "%s: Syntax error. Usage: \"guessnumber min max\" where min is the minimum value and max is the maximum value."
		self.startmessage = "Game of Guessnumber started with %s. Try guessing which number I am thinking of by saying a number."
		
	def prase_privmsg(self, event):
		nick, source = event.source.split("!")
		print nick
		print source
		channel = event.channel
		message = event.message
		
		if channel[0] != "#":
			channel = nick
		
		if self.games.has_key(source):
			self.games[source].process(event.message.split(":")[1], channel, nick)
			return
		
		if message.find(" ") == -1:  # If no parameters, discard
			if command == "guessnumber":
				self.evManager.post(SendPrivmsgEvent(channel, self.errormessage % (nick,)))
		command = message.split(" ")
		parameters = command[1:]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		
		if command == "guessnumber":
			if len(parameters) < 2:  # not enough parameters, output help
				self.evManager.post(SendPrivmsgEvent(channel, self.errormessage % (nick,)))
				return
			try:
				min = int(parameters[0])
				max = int(parameters[1])
			except ValueError:
				self.evManager.post(SendPrivmsgEvent(channel, self.errormessage % (nick,)))
				
			self.games[source] = Guessnumber(min, max, self.evManager, channel, nick)
			self.evManager.post(SendPrivmsgEvent(channel, self.startmessage % (nick, )))
	def notify(self, event):
		if isinstance(event, PrivmsgEvent):
			self.prase_privmsg(event)
		elif isinstance(event, ReloadconfigEvent):
			if event.module == "guessnumber" or event.module == "all":
				self.read_config()
		elif isinstance(event, TickEvent):
			self.check_instances()
			
			
	def check_instances(self):
		items = []
		for source, game in self.games.iteritems():
			if game.state == Guessnumber.STATE_STOPPED:
				items.append(source)
				
		for item in items:
			del self.games[item]
			
	def read_config(self):
		pass
		
		
class Guessnumber():
	STATE_STOPPED = 'stopped'
	STATE_RUNNING = 'running'
	def __init__(self, min, max, evManager, channel, nick):
		self.evManager = evManager
		self.state = Guessnumber.STATE_RUNNING
		self.number = random.randint(min, max)
		self.channel = channel
		self.nick = nick
		print self.number
		
	def process(self, message, channel, nick):
		if (self.channel[0] == "#" and channel != self.channel) or (self.channel[0] == "#" and channel[0] != "#") or (self.channel[0] != "#" and channel[0] == "#"):
			return
		try:
			print message
			value = int(message)
		except ValueError:
			self.evManager.post(SendPrivmsgEvent(channel, "Please enter a number."))
			return
		if value == self.number:  # game won
			self.evManager.post(SendPrivmsgEvent(channel, "Congratulations " + nick + " you have guessed the right number and therefore won the game!"))
			self.state = Guessnumber.STATE_STOPPED
		elif value > self.number:  # need to guess lower
			self.evManager.post(SendPrivmsgEvent(channel, nick + ": The number I'm looking for is lower."))
		elif value < self.number:  # need to guess higher
			self.evManager.post(SendPrivmsgEvent(channel, nick + ": The number I'm looking for is higher."))
			
			
			