#!/usr/bin/python
import spinner
import gui
import sys

"""
main.py
Start the bot with either GUI or Console.
"""

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1].lower() == "gui":
		gui.main()
	else:
		spinner.main()