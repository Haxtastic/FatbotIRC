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
import wx, time, thread, sys
from events import QuitEvent, DisconnectEvent, ParsedPrivmsgEvent
from weakboundmethod import WeakBoundMethod as Wbm
from eventdispatcher import EventDispatcher
from spinner import Spinner
		

class Form(wx.Panel):
	''' The Form class is a wx.Panel that creates a bunch of controls
		and handlers for callbacks. Doing the layout of the controls is 
		the responsibility of subclasses (by means of the doLayout()
		method). '''

	def __init__(self, *args, **kwargs):
		super(Form, self).__init__(*args, **kwargs)
		self.createControls()
		self.doLayout()
		self.loggerLock = thread.allocate_lock()

	def createControls(self):
		self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.editname = wx.TextCtrl(self)
		#for i in range(0, 23):
		#	 self.__log("\n")

	def doLayout(self):
		''' Layout the controls that were created by createControls(). 
			Form.doLayout() will raise a NotImplementedError because it 
			is the responsibility of subclasses to layout the controls. '''
		raise NotImplementedError

	# Helper method(s):

	def log(self, message):
		self.loggerLock.acquire()
		self.logger.AppendText(message+"\n")
		self.logger.ScrollLines(-1)
		self.loggerLock.release()


class FormWithSizer(Form):		
	def doLayout(self):
		''' Layout the controls by means of sizers. '''

		# A horizontal BoxSizer will contain the GridSizer (on the left)
		# and the logger text control (on the right):
		boxSizer = wx.BoxSizer(orient=wx.VERTICAL)

		# Prepare some reusable arguments for calling sizer.Add():
		expandOption = dict(flag=wx.EXPAND)
		noOptions = dict()
		emptySpace = ((0, 0), noOptions)

		boxSizer.Add(self.logger, border=5, flag=wx.ALL|wx.EXPAND, proportion=1)
		boxSizer.Add(self.editname, border=5, flag=wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.EXPAND)
		boxSizer.SetMinSize((800, 400))

		self.SetSizerAndFit(boxSizer)


class FrameWithForms(wx.Frame):
	def __init__(self, ed, *args, **kwargs):
		super(FrameWithForms, self).__init__(*args, **kwargs)
		self.tabs = ["main", "server", "bot", "internal"]
		self.ed = ed
		notebook = wx.Notebook(self)
		self.forms = dict()
		for tab in self.tabs:
			self.forms[tab] = FormWithSizer(notebook, name=tab.capitalize())
			self.forms[tab].editname.Bind(wx.EVT_CHAR_HOOK, self.onEnter)
			notebook.AddPage(self.forms[tab], tab.capitalize())
		self.SetClientSize(notebook.GetBestSize())
		self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
		
	def write(self, text):
		if len(text) <= 1 or " " not in text or ":" not in text:
			return
		time, origin = text.split(" ", 1)
		origin, message = origin.split(":", 1)
		message = time + message
		if origin.lower() in self.forms:
			self.forms[origin.lower()].log(message)
		self.forms[self.tabs[0]].log(text)
		
	def onEnter(self, event):
		if event.GetKeyCode()in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
			textctrl = event.GetEventObject()
			message = textctrl.GetValue().strip()
			if " " not in message:
				return
			textctrl.SetValue("")
			source = "Internal@Command"
			nick = ""
			channel = "Internal"
			command = message.split(" ")
			parameters = command[1:]
			command = command[0].lower()
			self.ed.post(ParsedPrivmsgEvent(nick, source, channel, message, command, parameters))
		else:
			event.Skip()

	def onCloseWindow(self, event):
		self.ed.post(DisconnectEvent("Can you see what's wrong?"))
			
class GUIWindow(wx.App):
	def OnInit(self):
		wx.App.__init__(self, False)
		self.ed = EventDispatcher()
		self.frame = FrameWithForms(self.ed, None, title='FatbotIRC GUI')
		sys.stdout = self.frame
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True
	
	def run(self):
		self.spinner = Spinner(self.ed)
		evtloop = wx.EventLoop()
		wx.EventLoop.SetActive(evtloop)
		
		self.spinner.bot.start()
		
		while self.spinner.alive is True:
			self.ed.consume_event_queue()
			while evtloop.Pending():
				evtloop.Dispatch()
				
			time.sleep(0.01)
			self.ProcessIdle()
	
			
def main():
	GUIWindow().run()
			
if __name__ == '__main__':
	main()
		