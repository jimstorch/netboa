#------------------------------------------------------------------------------
#   netboa/websocket/ws_client.py
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

from netboa.client import Client


class WsClient(Client):
    
    def __init__(self, sock, address, port):
        Client.__init__(self, sock, address, port)

    def get_raw_input(self):
        data = self.recv_buffer
        self.recv_buffer = ''
        return data

    def get_input(self):
        data = self.recv_buffer
        self.recv_buffer = ''
        return data.lstrip('\x00').rstrip('\xff')

    def send_raw(self, data):
        if data:
            self.send_buffer += data
            self.server._request_send(self)
    
    def send(self, data):
        if data:
            self.send_buffer += '\x00' + data + '\xFF'
            self.server._request_send(self)        
