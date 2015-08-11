"""
Copyright 2014 Magnus Briden

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from core import spinner, gui, eventdispatcher
import botinfo
import sys

"""
main.py
Start the bot with either GUI or Console.
"""

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Please start this program with at least 2 parameters"
        print "1. The core config file."
        print "2. The module config file"
        print "3. (Optional) GUI parameter to start with GUI, if ommited then bot will be run in terminal."
        exit()

    #botinfo.bot_info["ed"] = eventdispatcher.EventDispatcher()
    #botinfo.read_config("core", "config.cfg")
    #print botinfo.bot_info["core"]
    #if len(sys.argv) > 1 and sys.argv[1].lower() == "gui":
    #   gui.main()#botinfo.bot_info["ed"])
    #else:
        #spinner.main()#botinfo.bot_info["ed"])
