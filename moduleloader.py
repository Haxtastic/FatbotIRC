from modules import *

def load_modules(evManager):
	list = []
	#  Load your modules here
	list.append(protocolirc.protocolIRC(evManager))
	list.append(gamemanager.GameManager(evManager))
	list.append(youtubehelper.youtubeHelper(evManager))
	list.append(autopinger.autoPinger(evManager))
	list.append(performer.performer(evManager))
	list.append(nickserv.nickserv(evManager))
	return list