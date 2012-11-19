import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser
from games import *

class GameManager():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.read_config()
		self.games = {}
		self.started = False
		
	def parse_privmsg(self, event):
		if self.started == False:
			return
		nick, source = event.source.split("!")
		channel = event.channel
		message = event.message
		if channel[0] != "#":  # if the message isn't from a channel, the channel is the message owners nick
			channel = nick
		
		if self.games.has_key(source):  # if message owner is in a game, let the game process the info
			self.games[source].process(event.message.split(":")[1], channel, nick)
			return
			
		command = message.split(" ")
		parameters = command[1:]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		
		if command == "guessnumber":				
			self.games[source] = guessnumber.Guessnumber(self.evManager, channel, nick, parameters)
			
	def notify(self, event):
		if isinstance(event, PrivmsgEvent):
			self.parse_privmsg(event)
		elif isinstance(event, ReloadconfigEvent):
			if event.module == "games" or event.module == "all":
				self.read_config()
		elif isinstance(event, TickEvent):
			self.check_instances()
		elif isinstance(event, WelcomeEvent):
			self.started = True
			
			
	def check_instances(self):
		items = []
		for source, game in self.games.iteritems():
			if game.state == game.STATE_STOPPED:
				items.append(source)
				
		for item in items:
			del self.games[item]
			
	def read_config(self):
		pass
		