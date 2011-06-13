#!/usr/bin/env python
#------------------------------------------------------------------------------
#   test.py
#   Copyright 2011 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#------------------------------------------------------------------------------


#import gc
#from pprint import pprint
#gc.set_debug(gc.DEBUG_LEAK)
#def collect_and_show_garbage():
#    "Show what garbage is present."
#    print 'Unreachable:', gc.collect()
#    print 'Garbage:', pprint(gc.garbage)


from netboa import Server
from netboa import Service
from netboa.http import HttpService
from netboa.websocket import WebSocketService
from netboa.telnet import TelnetService

## Create our services
service = Service(port=7776)
telnet = TelnetService(port=7777)
websocket = WebSocketService(port=7778)
http = HttpService(port=7779)

## Create our server
server = Server((service, telnet, websocket, http))
#server = Server((websocket, http))


print '--> Starting Server.  Press CTRL-C to exit.'
while True:
    server.poll()
    #collect_and_show_garbage() 

