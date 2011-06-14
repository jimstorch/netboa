#------------------------------------------------------------------------------
#   netboa/websocket/handshake75.py
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

from netboa.websocket.ws_error import NetboaWsBadRequest


##  Sample Request
#   GET /demo HTTP/1.1\r\n
#   Upgrade: WebSocket\r\n
#   Connection: Upgrade\r\n
#   Host: example.com\r\n
#   Origin: http://example.com\r\n
#   WebSocket-Protocol: sample\r\n
#   \r\n


RESPONSE75 = (
    'HTTP/1.1 101 Web Socket Protocol Handshake\r\n'
    'Upgrade: WebSocket\r\n'
    'Connection: Upgrade\r\n'
    'WebSocket-Origin: %s\r\n'
    'WebSocket-Location: ws://%s:%d/\r\n'
    '\r\n'
    )

def parse_request75(request):

    print repr(request)

    req = {}
    segments = request.split('\r\n\r\n', 1)
    if len(segments) != 2:
        raise NetboaWsBadRequest('Empty or malformed ws request.')
    header, payload = segments
    lines = header.split('\r\n')
    if not lines:
        raise NetboaWsBadRequest('Missing request ws header.')
    line = lines.pop(0)
    items = line.split('\x20')
    if len(items) != 3:
        raise NetboaWsBadRequest('Malformed ws request method.')
    req['method'] = items[0]
    uri = items[1].lstrip('/')
    req['uri'] = uri
    req['version'] = items[2]
    for line in lines:
        parts = line.split(':\x20', 1)
        if len(parts) == 2:
            req[parts[0].lower()] = parts[1]
    req['payload'] = payload.rstrip('\r\n')
    return req    


def handshake75(client):
    request = client.get_input()
    req = parse_request75(request)
    origin = req.get('origin', None)
    if not origin:
        NetboaWsBadRequest('Missing origin field in ws request.')    
    host = req['host']
    parts = host.split(':')
    if len(parts) != 2:
        NetboaWsBadRequest('Malformed origin field in ws request.')    
    domain = parts[0]
    port = client.service.port
    ## WebSockets are very fussy; localhost:port != 127.0.0.1:port
    response = RESPONSE75 % (origin, domain, port)
    print response
    client.send_raw(response) 
    
    
