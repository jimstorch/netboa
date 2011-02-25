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
    lines = request.split('\r\n')
    if not lines:
        raise NetboaWsBadRequest('Empty Header.')
    line = lines.pop(0)
    items = line.split('\x20')
    print items
#    if len(items) != 3:
#        raise NetboaWsBadRequest('Method line is not 3 arguments.')
    req['method'] = items[0]
    uri = items[1]
    if uri.startswith('/'):
        uri = uri[1:]
    req['uri'] = uri
    req['version'] = items[2]
    for line in lines:
        parts = line.split(':\x20', 1)
        if len(parts) == 2:
            req[parts[0].lower()] = parts[1]
    return req
