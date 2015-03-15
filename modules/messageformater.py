from core.events import OutputEvent, NoticeEvent, ReginfoEvent, NoexistEvent, PrivmsgEvent, ModeEvent, JoinedEvent, PartedEvent, JoinEvent, PartEvent, SendPrivmsgEvent
from core.weakboundmethod import WeakBoundMethod as Wbm

class messageformater():
	def __init__(self, ed):
		self.ed = ed
		self.destination = "main"
		self.name = "Fatbot"
		self._connections = [
			self.ed.add(NoticeEvent, Wbm(self.parse_notice)),
			self.ed.add(ReginfoEvent, Wbm(self.parse_reginfo)),
			self.ed.add(NoexistEvent, Wbm(self.parse_noexist)),
			self.ed.add(PrivmsgEvent, Wbm(self.parse_privmsg)),
			self.ed.add(ModeEvent, Wbm(self.parse_mode)),
			self.ed.add(JoinedEvent, Wbm(self.parse_embargo)),
			self.ed.add(PartedEvent, Wbm(self.parse_embargo)),
			#self.ed.add(JoinEvent, Wbm(self.parse_embargo)),
			#self.ed.add(PartEvent, Wbm(self.parse_embargo)),
			self.ed.add(SendPrivmsgEvent, Wbm(self.parse_privmsg)),
		]
		
		
	def parse_notice(self, event):#, source, nick, type, dest, data):
		OutputEvent(self.destination, "[%c] %s" % (event.type[0], event.data)).post(self.ed)
		
	def parse_reginfo(self, event):#, source, nick, type, dest, data):
		OutputEvent(self.destination, "%s" % (event.data.lstrip(":"), )).post(self.ed)
	
	def parse_noexist(self, event):#, source, nick, type, dest, data):
		OutputEvent(self.destination, "There is no such nick/channel (%s)" % (event.dest, )).post(self.ed)
	
	def parse_privmsg(self, event):#, source, nick, type, dest, data):
		if "!" in event.source:
			nick, event.source = event.source.split("!")
		else:
			nick = event.source
		OutputEvent(event.dest, "[%s] %s" % (nick, event.data.lstrip(":"))).post(self.ed)
	
	def parse_mode(self, event):#, source, nick, type, dest, data):
		if "!" in event.source:
			nick, event.source = event.source.split("!")
		else:
			nick = event.source
		OutputEvent(self.destination, "%s sets %s %s on %s" % (nick, event.type, event.data, event.dest)).post(self.ed)
	
	def parse_embargo(self, event):#, source, nick, type, dest, data):
		if "!" in event.source:
			nick, event.source = event.source.split("!")
		else:
			nick = event.source
		OutputEvent(event.dest, "%s: %s(%s)" % (event.type.capitalize(), nick, event.source)).post(self.ed)
		
