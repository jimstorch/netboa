#------------------------------------------------------------------------------
#   netboa/websocket/handshake13.py
#   Copyright 2012 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#------------------------------------------------------------------------------

from hashlib import sha1
from base64 import b64encode

from netboa.websocket.ws_error import NetboaWsBadRequest
    

WS13_GUID = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

RESPONSE = (
    b'HTTP/1.1 101 Switching Protocols\r\n'
    b'Upgrade: websocket\r\n'
    b'Connection: Upgrade\r\n'
    b'Sec-WebSocket-Accept: {}\r\n'
    #b'Sec-WebSocket-Protocol: chat\r\n'
    b'\r\n'
    )

def parse_request(request):
    req = {}
    lines = request.split(b'\r\n')
    line = lines.pop(0)
    items = line.split(b'\x20',2)
    if len(items) != 3:
        raise NetboaWsBadRequest('[ws_lib] malformed WebSocket request.')
    req[b'method'] = items[0]
    req[b'request_uri'] = items[1]
    req[b'http_version'] = items[2]
    for line in lines:
        if line:
            parts = line.split(b':\x20', 1)
            req[parts[0].lower()] = parts[1].strip()
    version = req.get('sec-websocket-version', None)
    if version != '13':
        raise NetboaWsBadRequest('[ws_lib] wrong WebSocket version.')    
    return req

def handshake13(client):
    request = client.get_bytes()
    req = parse_request(request)
    salted_key = req[b'sec-websocket-key'] + WS13_GUID
    sec_ws_accept = b64encode(sha1(salted_key).digest())
    client.send_raw(RESPONSE.format(sec_ws_accept))

