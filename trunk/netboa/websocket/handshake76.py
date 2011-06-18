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

from netboa import bytes_to_str
from netboa.websocket.ws_error import NetboaWsBadRequest
from netboa.websocket.ws_lib import parse_request


def get_word(key):
    keystr = bytes_to_str(key)
    digits=''
    spaces=0
    for char in keystr:
        if char.isdigit():     
            digits += char
        elif char == '\x20':
            spaces += 1
    if not spaces or not digits:
        raise NetboaWsBadRequest('[76] Sec-WebSockets-Key malformed.')
    try:     
        keynum = int(digits)
    except ValueError:
        raise NetboaWsBadRequest('[76] Sec-WebSockets-Key bad integer.')  
    if (keynum % spaces != 0):
        raise NetboaWsBadRequest('[76] Sec-WebSockets-Key not divisible.') 
    wordval = int(keynum / spaces)
    if wordval >= 2 ** 32:
        raise NetboaWsBadRequest('[76] Sec-WebSockets-Key integer too large.')
    return struct.pack("!I", wordval)

def handshake76(client):
    request = client.get_bytes()
    req = parse_request(request)
    origin = req.get(b'origin', None)
    if not origin:
        raise NetboaWsBadRequest('[76] WebSocket request missing origin.')    
    host = req.get(b'host', None)
    if not host:
        raise NetboaWsBadRequest('[76] WebSocket request missing host.')   
    domain = host.split(b':')[0]
    key1 = req.get(b'sec-websocket-key1', None)
    key2 = req.get(b'sec-websocket-key2', None)
    if not key1 or not key2:
        raise NetboaWsBadRequest('[76] Missing Sec-WebSocket-Key in request.')
    word1 = get_word(key1)
    word2 = get_word(key2)
    salt = req.get(b'payload', None)
    if not salt:
        raise NetboaWsBadRequest('[76] WebSocket request missing salt.')
    if len(salt) != 8:
        raise NetboaWsBadRequest('[76] WebSocket salt incorrect length.')        
    token = hashlib.md5(word1 + word2 + salt).digest()  
    port = client.service.port
    response = b''.join((
        b'HTTP/1.1 101 WebSocket Protocol Handshake\r\n',
        b'Upgrade: WebSocket\r\n',
        b'Connection: Upgrade\r\n'
        b'Sec-WebSocket-Origin: ', origin, b'\r\n',
        b'Sec-WebSocket-Location: ws://', domain, b':', str(port).encode(), 
        b'/\r\n',
        b'Sec-WebSocket-Protocol: *\r\n',
        b'\r\n',
        token,        
        ))
    client.send_raw(response)

