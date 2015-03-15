# encoding: UTF-8
import os, sys
from core.events import *
from core.weakboundmethod import WeakBoundMethod as Wbm

class fridhemauth():
	def __init__(self, ed):
		self.ed = ed
		#self.read_config()
		self._connections = [
			self.ed.add(PrivmsgEvent, Wbm(self.parse_privmsg))
		]
		self.started = False
		
	def parse_privmsg(self, event):
		if self.started == False:
			return
		nick, source = event.source.split("!")
		channel = event.dest
		message = event.data
		
		# :Kek!Keke@somekind.ofspecial.mask PRIVMSG Fatbot :Hey
		if channel != "#opers" or message.find(":<xmlrpc> REGISTER:") == -1:
			return
		
		command = message.split(" ")
		parameters = command[1:]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		
		mess = "flags #fridhem.priv %s +vV" % (parameters[1][1:-1])
		#/msg chanserv flags #fridhem.priv nickpåreggadekontot +vV
		#self.ed.post(SendPrivmsgEvent("chanserv", mess, ""))
		SendPrivmsgEvent("chanserv", mess, "").post(self.ed)
		