import os, sys
from core.events import *
import ConfigParser
from games import *
from core.weakboundmethod import WeakBoundMethod as Wbm

class gamemanager():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self.games = {}
		self.started = False
		self._connections = [
			self.ed.add(PrivmsgEvent, Wbm(self.parse_privmsg)),
			self.ed.add(TickEvent, Wbm(self.check_instances))
		]
		
	def parse_privmsg(self, event):
		if "!" not in event.source or ":" not in event.data:
			return
		nick, source = event.source.split("!", 1)
		channel = event.dest
		message = event.data.split(":", 1)[1]
		if channel[0] != "#":  # if the message isn't from a channel, the channel is the message owners nick
			channel = nick
		
		if self.games.has_key(source):  # if message owner is in a game, let the game process the info
			self.games[source].process(message, channel, nick)
			return
		
		if " " not in event.data:
			return
			
		command = message.split(" ")
		parameters = command[1:]
		command = command[0].lower()  # Get rid of the : at start and no caps
		
		if command == "guessnumber":				
			self.games[source] = guessnumber.Guessnumber(self.ed, channel, nick, parameters)
	
	def reload_config(self, event):
		if event.module == "games" or event.module == "all":
			self.read_config()
			
	def check_instances(self, event):
		items = []
		for source, game in self.games.iteritems():
			if game.state == game.STATE_STOPPED:
				items.append(source)
				
		for item in items:
			del self.games[item]
			
	def read_config(self):
		pass
		