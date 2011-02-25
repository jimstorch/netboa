#------------------------------------------------------------------------------
#   netboa/http/http_service.py
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

from netboa.service import Service
from netboa.debug import debug_on_connect
from netboa.debug import debug_on_disconnect
from netboa.http.http_client import HttpClient
from netboa.http.http_handler import http_handler


def on_connect(client):
    #print('[HTTP] New Connection from %s' % client.origin) 
    pass

def on_disconnect(client):
    #print('[HTTP] Lost Connection from %s' % client.origin)
    pass 

def on_input(client):
    print('[HTTP] Input from %s' % client.origin)
    print client.get_input()

class HttpService(Service):
    def __init__(self, on_connect=on_connect, on_disconnect=on_disconnect,
            on_input=http_handler, port=7777,  address=''):
        Service.__init__(self, on_connect, on_disconnect, on_input, port,
            address)

