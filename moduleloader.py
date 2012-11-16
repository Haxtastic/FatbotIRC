from modules import *

def load_modules(evManager):
	list = []
	#  Load your modules here
	list.append(protocolirc.protocolIRC(evManager))
	list.append(gamemanager.GameManager(evManager))
	list.append(youtubehelper.youtubeHelper(evManager))
	return list