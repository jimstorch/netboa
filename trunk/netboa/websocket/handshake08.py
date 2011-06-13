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


##  Sample Request
#   GET /chat HTTP/1.1\r\n
#   Host: server.example.com\r\n
#   Upgrade: websocket\r\n
#   Connection: Upgrade\r\n
#   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n
#   Sec-WebSocket-Origin: http://example.com\r\n
#   Sec-WebSocket-Protocol: chat, superchat\r\n
#   Sec-WebSocket-Version: 8\r\n
#   \r\n


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
        raise NetboaWsBadRequest('Missing origin in WebSocket request.')    
    host = req.get('host', None)
    if not host:
        raise NetboaWsBadRequest('Missing host in WebSocket request.')   
    parts = host.split(':')
    if len(parts) != 2:
        raise NetboaWsBadRequest('Malformed origin in WebSocket request.')    
    domain = parts[0]
    port = client.service.port
    response = RESPONSE76 % (origin, domain, port, hashed)
    print repr(response)
    client.send(response)


def keygen08(request_key):
    combo = unicode(request_key + HANDSHAKE08_GUID)
    hashed = hashlib.sha1(combo).digest()
    accept_key = base64.b64encode(hashed)
    return accept_key
 
   
