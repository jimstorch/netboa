#------------------------------------------------------------------------------
#   netboa/websocket/handshake76.py
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

import struct
import hashlib
import base64

from netboa.websocket.ws_error import NetboaWsBadRequest
from netboa.websocket.ws_lib import parse_request


HANDSHAKE08_GUID = u'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

RESPONSE08 = (
    'HTTP/1.1 101 Switching Protocols\r\n'
    'Upgrade: websocket\r\n'
    'Connection: Upgrade\r\n'
    'Sec-WebSocket-Accept: %s\r\n'
    'Sec-WebSocket-Protocol: chat\r\n'
    '\r\n'
    )

def handshake08(client):
    request = client.get_input()
    print repr(request)
    req = parse_request(request)
    print repr(req)
    origin = req.get('origin', None)
    if not origin:
        raise NetboaWsBadRequest('[08] WebSocket request missing origin.')    
    host = req.get('host', None)
    if not host:
        raise NetboaWsBadRequest('[08] WebSocket request missing host.')   
    domain = host.split(':')[0]
    port = client.service.port
    key = req.get('sec-websocket-key', None)
    if not key:
        raise NetboaWsBadRequest('[08] WebSocket request missing key.')
    hashed = hashlib.sha1(unicode(key + HANDSHAKE08_GUID)).digest()
    token = base64.b64encode(hashed)
    response = RESPONSE08 % (origin, domain, port, token)
    print repr(response)
    client.send_raw(response)



 
   
