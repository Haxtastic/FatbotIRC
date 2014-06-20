from eventdispatcher import EventDispatcher
from spinner import Spinner

"""
main.py
Simply start the event dispatcher and run the spinner.
"""

def main():
	Spinner(EventDispatcher()).run()

if __name__ == '__main__':
	main()