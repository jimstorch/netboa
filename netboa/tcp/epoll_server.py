#------------------------------------------------------------------------------
#   netboa/tcp/epoll_server.py
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
Server that uses the Epoll API introduced in Linux kernel 2.5.44.
This is the default server for Linux.
"""

import select
import time

from netboa.tcp.tcp_error import NetboaConnectionLost


MAX_CONNECTIONS = 1000  

class EpollServer(object):

    def __init__(self, service=None):
        self.epoll = select.epoll()
        self.services = {}
        self.clients = {}
        self.drop_queue = set()
        if service is not None:    
            self.add_service(service)

    def add_service(self, service):
        if hasattr(service, '__iter__'):
            for a_service in service:
                self._register_service(a_service)
        else:
            self._register_service(service)        

    def _register_service(self, service):
        self.epoll.register(service.fileno(), select.EPOLLIN)
        self.services[service.fileno()] = service
        service.server = self

    def _add_client(self, client):
        self.clients[client.fileno()] = client
        self.epoll.register(client.fileno(), select.EPOLLIN)
        client.on_connect(client)

    def request_drop(self, client):
        self.drop_queue.add(client.fileno())

    def _drop_client_by_fileno(self, fileno):
        client = self.clients[fileno]
        client.on_disconnect(client)
        self.epoll.unregister(fileno)
        del self.clients[fileno]
        if fileno in self.drop_queue:
            self.drop_queue.remove(fileno)
        if hasattr(client, 'send_target'):
            del client.send_target
        if hasattr(client, 'recv_target'):
            del client.recv_target

    def _request_send(self, client):
        self.epoll.modify(client.fileno(), select.EPOLLIN | select.EPOLLOUT)

    def _clear_send(self, client):
        self.epoll.modify(client.fileno(), select.EPOLLIN)

    def poll(self):
        if self.drop_queue:
            for fileno in tuple(self.drop_queue):
                if not self.clients[fileno].has_output: 
                    self._drop_client_by_fileno(fileno)
        events = self.epoll.poll(.001)
        for fileno, event in events:
            if fileno in self.services:
                if len(self.clients) < MAX_CONNECTIONS:
                    client = self.services[fileno].create_client()
                    self._add_client(client)
                else:
                    print "Max connections"
            elif event & select.EPOLLIN:
                try:
                    self.clients[fileno]._socket_recv()
                except NetboaConnectionLost:
                    self._drop_client_by_fileno(fileno)
            elif event & select.EPOLLOUT:
                try:
                    self.clients[fileno]._socket_send()
                except NetboaConnectionLost:
                    self._drop_client_by_fileno(fileno)                   
            elif event & select.EPOLLHUP:
                if fileno in self.clients:
                    self._drop_client_by_fileno(fileno)

          
