from modules import *

def load_modules(evManager):
	list = []
	#  Load your modules here
	list.append(protocolirc.protocolIRC(evManager))
	list.append(guessnumber.GuessnumberManager(evManager))
	return list