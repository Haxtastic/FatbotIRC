import os, sys
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)
import botinfo
import wx, time, thread, multiprocessing as mp, spinner, re
from events import QuitEvent, RequestDisconnectEvent, ParsedPrivmsgEvent, Event, JoinEvent, PartEvent, RequestSendPrivmsgEvent
from weakboundmethod import WeakBoundMethod as Wbm


class Form(wx.Panel):
    ''' The Form class is a wx.Panel that creates a bunch of controls
        and handlers for callbacks. Doing the layout of the controls is
        the responsibility of subclasses (by means of the doLayout()
        method). '''

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.name = kwargs["name"]
        self.createControls()
        self.doLayout()
        self.loggerLock = thread.allocate_lock()

    def createControls(self):
        self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.TE_AUTO_URL|wx.TE_RICH)
        self.editname = wx.TextCtrl(self, name=self.name)

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
        self.logger.Refresh()
        self.loggerLock.release()

    def page_change(self, event):
        self.loggerLock.acquire()
        self.logger.AppendText("Paged changed")
        self.logger.ScrollLines(-1)
        self.logger.Refresh()
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
    def __init__(self, pipe, *args, **kwargs):
        super(FrameWithForms, self).__init__(*args, **kwargs)
        self.tabs = ["main", "server", "bot", "internal", "all"]
        self.n_tabs = len(self.tabs)
        self.pipe = pipe
        self.command_history = []
        self.command_position = 0
        self.currentTab = self.n_tabs
        self.regex = re.compile("[.]*->[.]*")
        self.notebook = wx.Notebook(self)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.page_change)
        self.forms = dict()
        for tab in self.tabs:
            self.forms[tab] = FormWithSizer(self.notebook, name=tab.capitalize())
            self.forms[tab].editname.Bind(wx.EVT_CHAR_HOOK, self.onEnter)#, self.forms[tab])
            self.notebook.AddPage(self.forms[tab], tab.capitalize())
            self.forms[tab].Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.forms[tab].page_change)
        self.SetClientSize(self.notebook.GetBestSize())
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.alive = True

    def page_change(self, event):
        if event.Selection >= self.n_tabs:
            self.currentTab = event.Selection

    def write(self, data):
        logAll = False
        if len(data) <= 1 or " " not in data or ":" not in data:
            return
        time, origin = data.split(" ", 1)
        origin, message = origin.split(":", 1)
        if len(self.regex.findall(message)) > 0:
            logAll = True
        message = time + message
        if origin.lower() in self.forms:
            self.forms[origin.lower()].log(message)
        if "main" not in origin.lower():
            self.forms[self.tabs[4]].log(data)
        if logAll and len(self.tabs) > self.n_tabs:
            self.forms[self.tabs[self.currentTab]].log(message)

    def onEnter(self, event):
        if event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            textctrl = event.GetEventObject()
            message = textctrl.GetValue().strip()
            while len(self.command_history) >= 500:
                self.command_history.pop(0)
            if len(self.command_history) < 1 or self.command_history[-1] != message:
                self.command_history.append(message)
            self.command_position = 0
            textctrl.SetValue("")
            if message.startswith("/") or textctrl.GetName().lower() in self.tabs[:self.n_tabs]:
                message = message.lstrip("/")
                if " " not in message:
                    return
                source = "Internal@Command"
                nick = ""
                channel = "Internal"
                command = message.split(" ")
                parameters = command[1:]
                command = command[0].lower()
                self.pipe.send(ParsedPrivmsgEvent(nick, source, channel, message, command, parameters))
            else:
                self.pipe.send(RequestSendPrivmsgEvent(textctrl.GetName(), message))
        elif event.GetKeyCode() in [wx.WXK_UP]:
            self.command_position+=1
            if self.command_position > len(self.command_history):
                self.command_position = len(self.command_history)
            textctrl = event.GetEventObject()
            command_index = len(self.command_history) - self.command_position
            try:
                textctrl.SetValue(self.command_history[command_index])
            except IndexError:
                textctrl.SetValue(str(command_index))
            textctrl.SetInsertionPointEnd()
        elif event.GetKeyCode() in [wx.WXK_DOWN]:
            textctrl = event.GetEventObject()
            self.command_position-=1
            if self.command_position < 1:
                self.command_position = 0
                textctrl.SetValue("")
                return
            command_index = len(self.command_history) - self.command_position
            textctrl.SetValue(self.command_history[command_index])
            textctrl.SetInsertionPointEnd()
        else:
            event.Skip()

    def onCloseWindow(self, event):
        self.pipe.send(RequestDisconnectEvent("Can you see what's wrong?"))
        self.alive = False

class GUIWindow(wx.App):
    def __init__(self, parameters):
        self.parameters = parameters
        config = botinfo.bot_info["Connection"];
        self.name = botinfo.bot_info["General"]["name"];
        self.server = "%s%s:%d" % (config["prefix"][1], config["ip"], config["port"][2])
        wx.App.__init__(self, False)
    def OnInit(self):
        self.parent_pipe, self.child_pipe = mp.Pipe()
        self.redirecter = bothandler(self.child_pipe, self.parameters)
        #self.redirecter.daemon = True
        self.redirecter.start()
        self.frame = FrameWithForms(self.parent_pipe, None, title='FatbotIRC as ' + self.name + " @ " + self.server)
        sys.stdout = self.frame
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def run(self):
        evtloop = wx.EventLoop()
        wx.EventLoop.SetActive(evtloop)

        while self.frame.alive:
            while evtloop.Pending():
                evtloop.Dispatch()
            while self.parent_pipe.poll():
                buffer = self.parent_pipe.recv()
                if not self.parse_event(buffer):
                    print buffer
            time.sleep(0.01)
            self.ProcessIdle()

    def parse_event(self, event):
        if isinstance(event, JoinEvent):
            tab = event.dest.lower()
            self.frame.tabs.append(tab)
            self.frame.forms[tab] = FormWithSizer(self.frame.notebook, name=tab.capitalize())
            self.frame.forms[tab].editname.Bind(wx.EVT_CHAR_HOOK, self.frame.onEnter)#, self.frame.forms[tab])
            self.frame.notebook.AddPage(self.frame.forms[tab], tab.capitalize())
            self.frame.notebook.SendSizeEvent()
            return False
        elif isinstance(event, PartEvent):
            tab = event.dest.lower()
            for index in range(self.frame.notebook.GetPageCount()):
                if self.frame.notebook.GetPageText(index).lower() == tab:
                    self.frame.forms.pop(tab)
                    self.frame.notebook.DeletePage(index)
                    self.frame.notebook.SendSizeEvent()
                    break
            #return True

class bothandler(mp.Process):

    def __init__(self, pipe, parameters):
        mp.Process.__init__(self)
        self.pipe = pipe
        self.parameters = parameters

    def run(self):
        sys.stdout = self
        spin = spinner.Spinner(self.parameters)
        self._con = [
            spin.ed.add(JoinEvent, Wbm(self.write)),
            spin.ed.add(PartEvent, Wbm(self.write))
        ]
        while spin.tick():
            if self.pipe.poll():
                self.pipe.recv().post(spin.ed)
            time.sleep(0.01)

    def write(self, data):
        self.pipe.send(data)
        return

    def flush(self):
        return


def main(parameters):
    fileName, coreFile, moduleFile, GUI = parameters;
    botinfo.bot_info.update(botinfo.read_config("core", coreFile))
    botinfo.bot_info.update(botinfo.read_config("modules", moduleFile))
    GUIWindow(parameters).run()









