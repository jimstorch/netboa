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

from netboa.websocket.ws_error import NetboaWsBadRequest
from netboa.websocket.ws_lib import parse_request


## Sample request
#   GET /demo HTTP/1.1\r\n
#   Host: example.com\r\n
#   Connection: Upgrade\r\n
#   Sec-WebSocket-Key2: 12998 5 Y3 1 .P00\r\n
#   Sec-WebSocket-Protocol: sample\r\n
#   Upgrade: WebSocket\r\n
#   Sec-WebSocket-Key1: 4 @1 46546xW%0l 1 5\r\n
#   Origin: http://example.com\r\n
#   \r\n 
#   ^n:ds[4U


RESPONSE76 = (
    'HTTP/1.1 101 WebSocket Protocol Handshake\r\n'
    'Upgrade: WebSocket\r\n'
    'Connection: Upgrade\r\n'
    'Sec-WebSocket-Origin: %s\r\n'
    'Sec-WebSocket-Location: ws://%s:%d/\r\n'
    'Sec-WebSocket-Protocol: *\r\n'
    '\r\n'
    '%s'
    )

def handshake76(client):
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
    key1 = req.get('sec-websocket-key1', None)
    key2 = req.get('sec-websocket-key1', None)
    if not key1 or not key2:
        raise NetboaWsBadRequest('Missing Sec-WebSocket-Key(s) in request.')
    key1_digits = ''
    key1_spaces = 0
    for char in key1:
        if char.isdigit():
            key1_digits += char
        elif char == '\x20':
            key1_spaces += 1
    key2_digits = ''
    key2_spaces = 0
    for char in key2:
        if char.isdigit():
            key2_digits += char
        elif char == '\x20':
            key2_spaces += 1
    if not key1_digits or not key2_digits:
        raise NetboaWsBadRequest('Sec-WebSocket-Key(s) missing digits.')     

    if not key1_spaces or not key2_spaces:
        raise NetboaWsBadRequest('Sec-WebSocket-Key(s) missing spaces.')      
    try:
        word1 = int(key1_digits) / key1_spaces
        word2 = int(key2_digits) / key2_spaces
    except ValueError:
        raise NetboaWsBadRequest('Sec-WebSockets-Key(s) bad integers.')       
    salt = req.get('payload', None)
    if not salt:
        raise NetboaWsBadRequest('WebSocket request missing salt.')    
    hashed = hashlib.md5(struct.pack('>II8s', word1, word2, salt)).digest()
    port = client.service.port
    response = RESPONSE76 % (origin, domain, port, hashed)
    print repr(response)
    client.send(response) 
   
