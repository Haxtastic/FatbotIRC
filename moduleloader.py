import pkgutil
import sys, os
from modules import *

def load_modules(evManager):
	list = []
	#  Load your modules here
	list.append(privmsgpraser.PrivmsgPraser(evManager))
	return list