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

import sys
import socket

from netboa import verbosity
from netboa.service import Service
from netboa.websocket.ws_client import WsClient
from netboa.websocket.ws_error import NetboaWsBadRequest
from netboa.websocket.handshake76 import handshake76


def tmp_on_connect(client):
    """Do nothing, pre-handshake placeholder."""
    client.server.vprint('[Pre-Negotiated WebSocket] New Connection from %s'
        % client.origin, verbosity.DEBUG )
    pass 

def tmp_on_disconnect(client):
    """Do nothing, pre-handshake placeholder."""
    client.server.vprint('[Pre-Negotiated WebSocket] Lost Connection with %s'
        % client.origin, verbosity.DEBUG) 
    pass 

def handshake(client):
    """Negotiate a persistent WebSocket with the browser -- OR DIE!"""
    client.server.vprint('[WebSocket Handshake] Request from %s' % 
        client.origin, verbosity.DEBUG)
    try:
        handshake76(client)
    except NetboaWsBadRequest as error:
        client.server.vprint('[WebSocket Error] %s' % error, verbosity.ERROR)
        client.deactivate()
    else:
        client.on_connect = client.service.active_on_connect
        client.on_input = client.service.active_on_input
        client.on_disconnect = client.service.active_on_disconnect
        client.on_connect(client)
        pass

def debug_on_connect(client):
    client.server.vprint('[WebSocket] New Connection from %s' % 
        client.origin, verbosity.INFO)

def debug_on_disconnect(client):
    print('[WebSocket] Lost Connection with %s' % client.origin, 
        verbosity.INFO) 

def debug_on_input(client):
    client.server.vprint('[WebSocket] Input from %s' % client.origin,
        verbosity.DEBUG)
    msg = client.get_string()
    #print repr(msg)
    client.send('Message Received: %s' % msg)


class WebSocketService(Service):

    def __init__(self, on_connect=debug_on_connect, 
            on_disconnect=debug_on_disconnect, on_input=debug_on_input,
            port=7778, address=''):
        ## This is plain ugly, but we need to hijack client events for the
        ## first exchange in order to carry out the WebSocket handshake.
        ## After that, we can treat it like an established client.
        Service.__init__(self, on_connect=tmp_on_connect,
            on_disconnect=tmp_on_disconnect, on_input=handshake,
            port=port, address=address)
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
