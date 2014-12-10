"""
Copyright 2014 Magnus Bridén

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
#!/usr/bin/python
import spinner
import gui
import sys

"""
main.py
Start the bot with either GUI or Console.
"""

if __name__ == '__main__':
	if(len(sys.argv) > 1 and sys.argv[1].lower() == "gui"):
		gui.main()
	else:
		spinner.main()