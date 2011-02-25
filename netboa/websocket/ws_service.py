#------------------------------------------------------------------------------
#   netboa/websocket/ws_service.py
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

#    Weirdness with local connections  
#    --------------------------------
#
#    In the Chrome address bar, you can specify: 

#        http://127.0.0.1:http_port
#        http://machine_name:http_port
#        http://localhost:http_port
#
#    and all will work because of some juggling performed in handshake75 to
#    match the Response host name to the WebSocket Request.
#
#    However, the Javascript part is kinda screwy.  

#        If I use 'ws://127.0.0.1:ws_port' it works.
#        If I use 'ws://machine_name:ws_port', it works.
#        If I use 'ws://localhost:ws_port', it doesn't even try to connect.
#
#    Apparently, this is a bug with Chrome & Chromium under Linux.


import sys
import socket

from netboa.service import Service
from netboa.websocket.ws_client import WsClient
from netboa.websocket.ws_error import NetboaWsBadRequest
from netboa.websocket.handshake75 import handshake75


def debug_on_input(client):
    print('[WEBSOCKET] Input from %s' % client.origin)
    print repr(client.get_input())
    client.send('Message Received')

def debug_on_connect(client):
    print('[WEBSOCKET] New Connection from %s' % client.origin)

def debug_on_disconnect(client):
    print('[WEBSOCKET] Lost Connection from %s' % client.origin) 

def tmp_on_connect(client):
    """Do nothing, pre-handshake placeholder."""
    print('[PRE-NEGOTIATED WEBSOCKET] New Connection from %s' % client.origin)
    pass 

def tmp_on_disconnect(client):
    """Do nothing, pre-handshake placeholder."""
    print('[PRE-NEGOTIATED WEBSOCKET] Lost Connection from %s' % client.origin) 
    pass 

def handshake(client):
    """Negotiate a persistent WebSocket with the browser -- OR DIE!"""
    print('[WEBSOCKET HANDSHAKE] Input from %s' % client.origin)
    try:
        handshake75(client)
    except NetboaWsBadRequest, error:
        print('[WEBSOCKET ERROR] %s' % error)
        client.deactivate()
    else:
        client.on_connect = client.service.active_on_connect
        client.on_input = client.service.active_on_input
        client.on_disconnect = client.service.active_on_disconnect
        client.on_connect(client)


class WsService(Service):

    def __init__(self, on_connect=debug_on_connect, 
            on_disconnect=debug_on_disconnect, on_input=debug_on_input,
            port=7778, address=''):
        ## This is plain ugly, but we need to hijack client events for the
        ## first exchange in order to carry out the WebSocket handshake.
        ## After that, we can treat it like an established client.
        Service.__init__(self, tmp_on_connect, tmp_on_disconnect, handshake,
            port, address)
        self.active_on_connect = on_connect
        self.active_on_input = on_input
        self.active_on_disconnect = on_disconnect
    
    def create_client(self):
        sock, (address, port) = self.sock.accept()
        client = WsClient(sock, address, port)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_input = self.on_input
        client.server = self.server
        client.service = self
        return client
