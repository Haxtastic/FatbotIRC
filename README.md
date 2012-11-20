Welcome to Fatbot Slim for IRC!

This bot is a hobby project of mine.  
This project is one of my first in Python(Wrote a chat server and client before this.)  

Tried to fit it into the MVC-pattern, but realized that I've made a huge mistake and will now continue with this junk.

It should be easy adding a new module to the bot.  
  
The bot will send out events for everything that happens with the appropriate information, currently:  
   
PRIVMSG  
  This event gets sent out when a PRIVMSG is received.  
  It is sent out with the data: soucre, channel, message, command, parameters.  
   
   
   
PING  
  This event gets sent out when the server pings the bot.  
  The pong message is automatically handled by the bot.  
  This event has no data.  
   
   
   
JOIN  
  This event is sent out when you tell the bot to join a channel.  
  It is sent out with the data: channel  

PART  
  This event is sent out when you tell the bot to leave a channel.  
  It is sent out with the data: channel  
  
  
  
You can create your own events by adding them to events.py  
You can then send out the event by registering a listener to the EventManager and posting the event.  
How you do this can be viewed in the source of most files.  