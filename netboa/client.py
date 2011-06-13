#------------------------------------------------------------------------------
#   netboa/client.py
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

import time
import socket

from netboa.tcp.tcp_error import NetboaConnectionLost


class Client(object):
    """
    Base Client Class.
    """
    def __init__(self, sock, address, port):
        self.fd = sock.fileno()
        self.sock = sock
        self.address = address
        self.port = port
        self.origin = '%s:%d' % (address, port)
        self.send_buffer = ''
        self.recv_buffer = ''
        self.connect_time = time.time()
        self.last_input_time = self.connect_time
        self.on_connect = None
        self.on_disconnect = None
        self.on_input = None
        self.server = None
        self.service = None

    def deactivate(self):
        self.server.request_drop(self)

    def fileno(self):
        return self.fd

    def send(self, data):
        if data:
            self.send_buffer += data
            self.server._request_send(self)

    def get_char(self):
        if self.recv_buffer:
            return self.recv_buffer.pop()
        else:
            return None

    def get_input(self):
        data = self.recv_buffer
        self.recv_buffer = ''
        return data

    def idle(self):
        return time.time() - self.last_input_time

    def duration(self):
        return time.time() - self.connect_time

    def has_output(self):
        return len(self.send_buffer) > 0

    def _socket_send(self):
        size = len(self.send_buffer)
        try:
            sent = self.sock.send(self.send_buffer)
        except socket.error:
            raise NetboaConnectionLost()
        if sent < size:
            self.send_buffer = self.send_buffer[sent:]
        else:
            self.send_buffer = ''
            self.server._clear_send(self)

    def _socket_recv(self):
        try:
            data = self.sock.recv(2048)
        except socket.error:
            raise NetboaConnectionLost()
        size = len(data)
        if size == 0:
            raise NetboaConnectionLost()
        self.last_input_time = time.time()
        self.recv_buffer += data
        self.on_input(self)



