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
import sys, time
from core.events import ReloadEvent
"""
Our module loader class.
It loads modules and reloads them simply put.
"""

def load_modules(ed):
    from modules import protocolirc, gamemanager, autopinger, performer, nickserv, privmsgparser, responder, messageformater
    #urlparser
    list = []
    #  Load your modules here
    list.append(protocolirc.protocolirc(ed))
    list.append(gamemanager.gamemanager(ed))
    #list.append(urlparser.urlparser(ed))
    list.append(autopinger.autopinger(ed))
    list.append(performer.performer(ed))
    list.append(nickserv.nickserv(ed))
    #list.append(oper.oper(ed))
    #list.append(fridhemauth.fridhemauth(ed))
    list.append(privmsgparser.privmsgparser(ed))
    list.append(messageformater.messageformater(ed))
    list.append(responder.responder(ed))
    return list
    
def reload_modules(list, ed):
    for module in list:
        name = module.__class__.__name__
        del module
        reload(sys.modules['modules.' + name])
    list = load_modules(ed)
    ReloadEvent().post(ed)
    return list     
