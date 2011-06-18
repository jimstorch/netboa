#------------------------------------------------------------------------------
#   netboa/websocket/ws_lib.py
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


def parse_request(request):
    req = {}
    segments = request.split(b'\r\n\r\n', 1)
    if len(segments) != 2:
        raise NetboaWsBadRequest(b'Empty or malformed WebSocket request.')
    header, payload = segments
    lines = header.split(b'\r\n')
    line = lines.pop(0)
    items = line.split(b'\x20',2)
    if len(items) != 3:
        raise NetboaWsBadRequest(b'Malformed WebSocket request method.')
    req[b'method'] = items[0]
    req[b'request_uri'] = items[1]
    req[b'http_version'] = items[2]
    for line in lines:
        parts = line.split(b':\x20', 1)
        assert(len(parts) == 2)
        req[parts[0].lower()] = parts[1]
    req[b'payload'] = payload
    return req
    ## Guess the version number
#    if 'version' not in req:
#        if 'sec-websocket-key2' in req:
#            req['version'] = 'draft76'
#        else:
#            req['version'] = 'draft75'
#    return req
