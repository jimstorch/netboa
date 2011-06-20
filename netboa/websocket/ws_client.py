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

from netboa import str_to_bytes
from netboa import bytes_to_str
from netboa.client import Client


class WsClient(Client):
    
    def __init__(self, sock, address, port):
        Client.__init__(self, sock, address, port)

    def get_string(self):
        data = bytes_to_str(self.get_bytes())
        return data.lstrip('\x00').rstrip('\xff')

    def send_raw(self, data):
        if type(data) == str:
            self.send_buffer += str_to_bytes(data)
        else:
            self.send_buffer += data
        self.server._request_send(self)
    
    def send(self, data):
        self.send_raw(b'\x00')
        self.send_raw(data)
        self.send_raw(b'\xff')
       