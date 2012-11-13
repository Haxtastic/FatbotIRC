from events import *
from eventmanager import EventManager
from bot import Bot
from spinner import CPUSpinnerController
#from console import ConsoleView

#from chat import ChatController, ChatView

def main():
	eventManager = EventManager()
	spinner = CPUSpinnerController(eventManager)
	#console = ConsoleView(eventManager)
	#chatView = ChatView(eventManager)
	#chatControl = ChatController(eventManager)
	bot = Bot("Fatbot", "irc.tweaknet.org", 6667, eventManager)
	spinner.run()

if __name__ == '__main__':
	main()