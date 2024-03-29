#------------------------------------------------------------------------------
#   netboa/http/http_service.py
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

import os
import sys
import socket

from netboa import verbosity
from netboa.service import Service
from netboa.http.http_client import HttpClient
from netboa.http.http_error import NetboaHttpBadRequest
from netboa.http.http_lib import parse_request
from netboa.http.http_lib import get_content_type
from netboa.http.http_lib import respond_200
from netboa.http.http_lib import respond_400
from netboa.http.http_lib import respond_404
from netboa.http.http_lib import respond_501


def on_connect(client):
    client.server.vprint('[HTTP] New Connection from %s' % client.origin,
        verbosity.DEBUG) 
    pass

def on_disconnect(client):
    client.server.vprint('[HTTP] Lost Connection with %s' % client.origin,
        verbosity.DEBUG)
    pass 

def debug_on_input(client):
    client.server.vprint('[HTTP] Request from %s' % client.origin,
        verbosity.DEBUG)

def http_on_input(client):
    request = client.get_bytes()
    #print(repr(request))
    try:
        req = parse_request(request)
    except NetboaHttpBadRequest as error:
        respond_400(client, error)
        client.server.vprint('[HTTP] 400 Bad Request Error', verbosity.ERROR)
    else:
        if req['method'] == b'GET':
            uri = req['uri']
            if uri == b'':
                filename = b'index.html'
            else:
                filename = uri            
            content_type = get_content_type(filename)
            path = os.path.join(b'./public_html', filename)
            if not os.path.isfile(path):
                respond_404(client)
                client.server.vprint('[HTTP] 404 NOT FOUND: %s' % 
                    path.decode(), verbosity.WARN) 
            else:
                client.server.vprint('[HTTP] GET %s' % path.decode(),
                    verbosity.INFO)
                content = open(path, 'rb').read()
                respond_200(client, content_type,  filename, len(content))
                client.send(content)
        else:
            respond_501(client)
            client.server.vprint('[HTTP] 501 Not Implemented Error', 
                verbosity.ERROR)
    finally:
        client.deactivate()

class HttpService(Service):
    def __init__(self, on_connect=on_connect, on_disconnect=on_disconnect,
            on_input=http_on_input, port=7777,  address=''):
        Service.__init__(self, on_connect, on_disconnect, on_input, port,
            address)

