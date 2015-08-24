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
# encoding: UTF-8
from core.events import OutputEvent, NoticeEvent, ReginfoEvent, NoexistEvent, PrivmsgEvent, ModeEvent, JoinedEvent, PartedEvent, JoinEvent, PartEvent, SendPrivmsgEvent
from core.weakboundmethod import WeakBoundMethod as Wbm
import os, sys
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)
from botinfo import bot_info

class messageformater():
    def __init__(self, ed):
        self.ed = ed
        self.destination = "main"
        self.read_config()
        self._connections = [
            self.ed.add(NoticeEvent, Wbm(self.parse_notice)),
            self.ed.add(ReginfoEvent, Wbm(self.parse_reginfo)),
            self.ed.add(NoexistEvent, Wbm(self.parse_noexist)),
            self.ed.add(PrivmsgEvent, Wbm(self.parse_privmsg)),
            self.ed.add(ModeEvent, Wbm(self.parse_mode)),
            self.ed.add(JoinedEvent, Wbm(self.parse_embargo)),
            self.ed.add(PartedEvent, Wbm(self.parse_embargo)),
            #self.ed.add(JoinEvent, Wbm(self.parse_embargo)),
            #self.ed.add(PartEvent, Wbm(self.parse_embargo)),
            self.ed.add(SendPrivmsgEvent, Wbm(self.parse_privmsg)),
        ]


    def parse_notice(self, event):#, source, nick, type, dest, data):
        OutputEvent(self.destination, "[%c] %s" % (event.type[0], event.data)).post(self.ed)

    def parse_reginfo(self, event):#, source, nick, type, dest, data):
        OutputEvent(self.destination, "%s" % (event.data.lstrip(":"), )).post(self.ed)

    def parse_noexist(self, event):#, source, nick, type, dest, data):
        OutputEvent(self.destination, "There is no such nick/channel (%s)" % (event.dest, )).post(self.ed)

    def parse_privmsg(self, event):#, source, nick, type, dest, data):
        source = nick = data =  ""
        data = event.data.lstrip(":")
        if "!" in event.source: #Priv msg
            source, event.source = event.source.split("!")
            nick = self.name
        elif self.name == event.source:
            source = self.name
            nick = event.dest
        if event.dest.startswith("#"): #Channel msg
            OutputEvent(event.dest, "[%s] %s" % (source, data)).post(self.ed)
            return
        OutputEvent(self.destination, "[%s] -> [%s] %s" % (source, nick, data)).post(self.ed)

    def parse_mode(self, event):#, source, nick, type, dest, data):
        if "!" in event.source:
            nick, event.source = event.source.split("!")
        else:
            nick = event.source
        OutputEvent(self.destination, "%s sets %s %s on %s" % (nick, event.type, event.data, event.dest)).post(self.ed)

    def parse_embargo(self, event):#, source, nick, type, dest, data):
        if "!" in event.source:
            nick, event.source = event.source.split("!")
        else:
            nick = event.source
        OutputEvent(event.dest, "%s: %s(%s)" % (event.type.capitalize(), nick, event.source)).post(self.ed)

    def read_config(self):
        self.name       = bot_info["General"]["name"]

