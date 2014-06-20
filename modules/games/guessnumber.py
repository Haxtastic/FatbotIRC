import os, sys
lib_path = os.path.abspath(os.path.join("..", "..", "core"))
sys.path.append(lib_path)
import random
from events import *
from weakboundmethod import WeakBoundMethod as Wbm

class Guessnumber():
	def __init__(self, ed, channel, nick, parameters):
		self.STATE_STOPPED = 'stopped'
		self.STATE_RUNNING = 'running'
		self.MESSAGE_ERROR = "%s: Syntax error. Usage: \"guessnumber min max\" where min is the minimum value and max is the maximum value."
		self.MESSAGE_START = "Game of Guessnumber started with %s. Try guessing which number I am thinking of by saying a number."
		self.ed = ed
		self.state = self.STATE_STOPPED
		self.realchannel = channel
		self.nick = nick
		self.tries = 0
		if self.realchannel[0] != "#":
			self.channel = nick
		else:
			self.channel = self.realchannel
			
		if len(parameters) < 2:  # not enough parameters, output help
			self.ed.post(SendPrivmsgEvent(channel, self.MESSAGE_ERROR % (nick,)))
			return
		try:
			min = int(parameters[0])
			max = int(parameters[1])
		except ValueError:
			self.ed.post(SendPrivmsgEvent(channel, self.MESSAGE_ERROR % (nick,)))
			return
		self.number = random.randint(min, max)
		self.ed.post(SendPrivmsgEvent(channel, self.MESSAGE_START % (nick, )))
		self.state = self.STATE_RUNNING
		
	def process(self, message, channel, nick):
		if channel != self.realchannel:
			return
			
		try:
			#print message
			value = int(message)
		except ValueError:
			#self.ed.post(SendPrivmsgEvent(self.channel, "Please enter a number."))
			return
			
		self.tries+=1
			
		if value == self.number:  # game won
			self.ed.post(SendPrivmsgEvent(self.channel, "Congratulations " + nick + " you have guessed the right number and therefore won the game!"))
			self.ed.post(SendPrivmsgEvent(self.channel, "It only took you %d tries!" % (self.tries, )))
			self.state = self.STATE_STOPPED
		elif value > self.number:  # need to guess lower
			self.ed.post(SendPrivmsgEvent(self.channel, nick + ": The number I'm thinking of is lower."))
		elif value < self.number:  # need to guess higher
			self.ed.post(SendPrivmsgEvent(self.channel, nick + ": The number I'm thinking of is higher."))
			
			
			