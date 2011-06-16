#------------------------------------------------------------------------------
#   netboa/tcp/select_server.py
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

"""
Server that uses the classic Select API to monitor sockets.
This is the default server for non-Linux environments.
"""

import sys
import select

from netboa import verbosity
from netboa.tcp.tcp_error import NetboaConnectionLost


if sys.platform == 'win32':
    MAX_CONNECTIONS = 500
else:
    MAX_CONNECTIONS = 1000

class SelectServer(object):

    def __init__(self, service=None):
        self.services = []
        self.clients = []
        self.senders = []
        self.drop_queue = set()
        if service is not None:
            self.add_service(service)
        self.verbosity = verbosity.ERROR

    def vprint(self, msg, level=verbosity.INFO):
        if level >= self.verbosity:
            print(msg)


    def add_service(self, service):
        if getattr(service, '__iter__', False):
            for a_serv in service:
                self._register_service(a_serv)
        else:
            self._register_service(service)   

    def _register_service(self, service):
        self.services.append(service)
        service.server = self

    def _add_client(self, client):
        self.clients.append(client)
        client.on_connect(client)

    def request_drop(self, client):
        self.vprint("[select] Client drop requested", verbosity.DEBUG)
        self.drop_queue.add(client)

    def _drop_client(self, client):
        client.on_disconnect(client)
        self.clients.remove(client)
        if client in self.senders:
            self.senders.remove(client)
        if client in self.drop_queue:
            self.drop_queue.remove(client)

    def _request_send(self, client):
        if client not in self.senders:
            self.senders.append(client)

    def _clear_send(self, client):
        if client in self.senders:
            self.senders.remove(client)

    def poll(self):
        if self.drop_queue:
            for client in tuple(self.drop_queue):
                if not client.has_output():
                    self._drop_client(client)
        readers, senders, errors = select.select(self.services + self.clients, 
            self.senders, [], .005)
        for reader in readers:
            if reader in self.services:
                if len(self.clients) < MAX_CONNECTIONS:
                    client = reader.create_client()                            
                    self._add_client(client)
                else:
                    self.vprint("[select] MAX CONNECTIONS", verbosity.WARN) 
            else:
                try:
                    reader._socket_recv()
                except NetboaConnectionLost:
                    self.vprint("[select] Could not read socket", 
                        verbosity.DEBUG)
                    self._drop_client(reader)
        for sender in senders:
            try:
                sender._socket_send()    
            except NetboaConnectionLost:
                self.vprint("[select] Could not write socket",
                    verbosity.ERROR)            
                self._drop_client(sender)

