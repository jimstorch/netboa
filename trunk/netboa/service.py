#------------------------------------------------------------------------------
#   netboa/service.py
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

from netboa.client import Client
from netboa.debug import debug_on_connect
from netboa.debug import debug_on_input
from netboa.debug import debug_on_disconnect

class Service(object):
    def __init__(self, on_connect=debug_on_connect, 
            on_disconnect=debug_on_disconnect, on_input=debug_on_input,
            port=7777,  address=''):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((address, port))
        sock.listen(5)
        sock.setblocking(0)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.fd = sock.fileno()
        self.sock = sock
        self.port = port
        self.address = address
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_input = on_input
        self.server = None

    def fileno(self):
        return self.fd

    def create_client(self):
        sock, (address, port) = self.sock.accept()
        client = Client(sock, address, port)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_input = self.on_input
        client.server = self.server
        client.service = self
        return client


