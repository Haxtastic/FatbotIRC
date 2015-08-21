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
import botinfo
import sys
from core import gui, spinner

"""
main.py
Start the bot with either GUI or Console.
"""

if __name__ == '__main__':
    parameters = sys.argv
    if len(parameters) < 3:
        print "Please start this program with at least 2 parameters"
        print "1. The core config file."
        print "2. The module config file"
        print "3. (Optional) If this parameters is equal to gui then bot won't be run in a terminal."
        exit()
    if len(parameters) < 4:
        parameters.append("no")

    fileName, coreFile, moduleFile, GUI = parameters;

    #botinfo.bot_info["ed"] = eventdispatcher.EventDispatcher()
    #print botinfo.bot_info["core"]
    if GUI.lower() == "gui":
        gui.main(parameters)
    else:
        spinner.main(parameters)
    #print botinfo.bot_info["core"]
    #if len(sys.argv) > 1 and sys.argv[1].lower() == "gui":
    #   gui.main()#botinfo.bot_info["ed"])
    #else:
        #spinner.main()#botinfo.bot_info["ed"])
