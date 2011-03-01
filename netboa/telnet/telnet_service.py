#------------------------------------------------------------------------------
#   netboa/telnet/telnet_service.py
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

import sys
import socket

from netboa.coroutine import coroutine
from netboa.service import Service
from netboa.telnet.telnet_client import TelnetClient


def debug_on_connect(client):
    print('[Telnet] New Connection from %s' % client.origin)

def debug_on_disconnect(client):
    print('[Telnet] Lost Connection from %s' % client.origin) 

def debug_on_input(client):
    print('[Telnet] Input from %s' % client.origin)
    print repr(client.get_input())
    client.send('Message Received\r\n')









class TelnetService(Service):

    def __init__(self, on_connect=debug_on_connect, 
            on_disconnect=debug_on_disconnect, on_input=debug_on_input,
            port=7778, address=''):
        Service.__init__(self, on_connect, on_disconnect, on_input, port,
            address)
