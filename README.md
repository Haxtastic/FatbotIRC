Welcome to Fatbot Slim for IRC!

Fatbot IRC is a bot I've been working on and off on for the last two years, it's designed to be very modular and the core part of the bot basically does nothing without any modules.  
It's a event-driven bot, the core part of the bot only handles the connection and specific types of input and sends these out as a event for some other part of the bot to process.  
Without any modules all the bot does is connect to the server and tells the server who we are, then it proceeds to send out events depending on what the server input is.  
The modules have access to whatever events they register to.  
There are a lot of different events and it's very easy to add another.  
Modules register what events they want to get notified about and when that event is fired the desired method is called with the appropriate data.  

Before running you need to install the external dependencies from External Support file.  

To run terminal just run main.py.  
To run with GUI (wxPython) then you can either run gui.py or main.py with parameter gui, e.g. "python main.py gui"  
  
The bot will send out events when things happens, there are several events.  
  
You can find and create your own events by adding them to events.py  
You can then send out the event by registering a listener to the EventManager and posting the event.  
How you do this can be viewed in the source of most files.  

Fatbot Slim for IRC is licensed under the [Apache 2 License](http://www.apache.org/licenses/LICENSE-2.0.html), meaning you
can use it free of charge, without strings attached in commercial and non-commercial projects.
