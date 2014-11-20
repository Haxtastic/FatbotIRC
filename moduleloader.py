import modules
import sys, time
from events import WelcomeEvent, OutputEvent
"""
Our module loader class.
It loads modules and reloads them simply put.
"""

def load_modules(ed):
	from modules import protocolirc, gamemanager, autopinger, performer, nickserv, privmsgparser, youtubehelper, reloadconfigresponder
	list = []
	#  Load your modules here
	list.append(protocolirc.protocolirc(ed))
	list.append(gamemanager.gamemanager(ed))
	list.append(youtubehelper.youtubehelper(ed))
	list.append(autopinger.autopinger(ed))
	list.append(performer.performer(ed))
	#list.append(nickserv.nickserv(ed))
	#list.append(oper.oper(ed))
	#list.append(fridhemauth.fridhemauth(ed))
	list.append(privmsgparser.privmsgparser(ed))
	list.append(reloadconfigresponder.reloadconfigresponder(ed))
	return list
	
def reload_modules(list, ed):
	for module in list:
		name = module.__class__.__name__
		del module
		reload(sys.modules['modules.' + name])
	list = load_modules(ed)
	ed.post(WelcomeEvent("modulereload"))
	return list
	
		
