import os, sys
#lib_path = os.path.abspath(os.path.join("..", "..", "core"))
#sys.path.append(lib_path)
import random
from core.events import *
from core.weakboundmethod import WeakBoundMethod as Wbm

class Guessnumber():
	MESSAGE_WIN 		= "Congratulations %s you have guessed the right number and therefore won the game!"
	MESSAGE_TRIES		= "It only took you %d tries!"
	MESSAGE_ERROR 		= "%s: Syntax error. Usage: \"guessnumber min max\" where min is the minimum value and max is the maximum value."
	MESSAGE_START 		= "Game of Guessnumber started with %s. Try guessing which number I am thinking of by saying a number."
	MESSAGE_LOWER		= "%s: The number I'm thinking of is lower."
	MESSAGE_HIGHER		= "%s: The number I'm thinking of is higher."
	MESSAGE_INTERNAL 	= "Game of Guessnumber started with %s, number is %d."
	
	def __init__(self, ed, channel, nick, parameters):
		self.STATE_STOPPED = 'stopped'
		self.STATE_RUNNING = 'running'
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
			RequestSendPrivmsgEvent(channel, Guessnumber.MESSAGE_ERROR % (nick,)).post(self.ed)
			return
		try:
			min = int(parameters[0])
			max = int(parameters[1])
		except ValueError:
			RequestSendPrivmsgEvent(channel, Guessnumber.MESSAGE_ERROR % (nick,)).post(self.ed)
			return
		self.number = random.randint(min, max)
		RequestSendPrivmsgEvent(channel, Guessnumber.MESSAGE_START % (nick, )).post(self.ed)
		OutputEvent("Internal", Guessnumber.MESSAGE_INTERNAL % (nick, self.number)).post(self.ed)
		self.state = self.STATE_RUNNING
		
	def process(self, message, channel, nick):
		if channel != self.realchannel:
			return
			
		try:
			value = int(message)
		except ValueError:
			return

		self.tries+=1
			
		if value == self.number:  # game won
			RequestSendPrivmsgEvent(self.channel, Guessnumber.MESSAGE_WIN % (nick, )).post(self.ed)
			RequestSendPrivmsgEvent(self.channel, Guessnumber.MESSAGE_TRIES % (self.tries, )).post(self.ed)
			self.state = self.STATE_STOPPED
		elif value > self.number:  # need to guess lower
			RequestSendPrivmsgEvent(self.channel, Guessnumber.MESSAGE_LOWER % (nick, )).post(self.ed)
		elif value < self.number:  # need to guess higher
			RequestSendPrivmsgEvent(self.channel, Guessnumber.MESSAGE_HIGHER % (nick, )).post(self.ed)
			
			
			