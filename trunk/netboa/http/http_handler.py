#------------------------------------------------------------------------------
#   netboa/http/http_handler.py
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

from netboa.http.http_error import NetboaHttpBadRequest
from netboa.http.http_lib import parse_request
from netboa.http.http_lib import get_content_type
from netboa.http.http_methods import respond_200
from netboa.http.http_methods import respond_400
from netboa.http.http_methods import respond_404
from netboa.http.http_methods import respond_501


def http_handler(client):
    request = client.get_input()
    try:
        req = parse_request(request)
        #print request
        #print repr(req)
    except NetboaHttpBadRequest, error:
        respond_400(client, error)
    else:
        if req['method'] == 'GET':
            uri = req['uri']
            if uri == '':
                filename = 'index.html'
            else:
                filename = uri            
            content_type = get_content_type(filename)
            path = os.path.join('./public_html', filename)
            if not os.path.isfile(path):
                respond_404(client)
            else:
                #print('[HTTP] GET %s' % path)
                content = open(path, 'rb').read()
                respond_200(client, content_type,  filename, len(content))
                client.send(content)
        else:
            respond_501(client)
    finally:
        client.deactivate()
