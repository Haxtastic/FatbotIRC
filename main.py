#!/usr/bin/python
from core import spinner, gui#, eventdispatcher, botinfo
import sys

"""
main.py
Start the bot with either GUI or Console.
"""

if __name__ == '__main__':
	#botinfo.bot_info["ed"] = eventdispatcher.EventDispatcher()
	if len(sys.argv) > 1 and sys.argv[1].lower() == "gui":
		gui.main()#botinfo.bot_info["ed"])
	else:
		spinner.main()#botinfo.bot_info["ed"])
