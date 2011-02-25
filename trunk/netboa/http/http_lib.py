#------------------------------------------------------------------------------
#   netboa/http/http_lib.py
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
import datetime

from netboa.http.http_error import NetboaHttpBadRequest


METHODS = ('HEAD', 'GET', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 
    'CONNECT', 'PATCH')

CONTENT_TYPES = {
    '.html':'text/html',
    '.htm':'text/html',
    '.css':'text/css',
    '.txt':'text/plain',
    '.js':'text/javascript',
    '.png':'image/png',
    '.jpg':'image/jpeg',
    '.gif':'image/gif',
    '.svg':'image/svg+xml',
    '.svgz':'image/svg+xml\r\nContent-Encoding: gzip',  ## omg hack
    '.ico':'image/x-icon',
    '.pdf':'application/pdf',
    }

def get_content_type(filename):
    foo, extension = os.path.splitext(filename)
    return CONTENT_TYPES.get(extension.lower(), 'application/x-unknown')

def parse_request(request):
    req = {}
    segments = request.split('\r\n\r\n', 1)
    if len(segments) != 2:
        raise NetboaHttpBadRequest('Missing header or terminator.') 
    header = segments[0]
    payload = segments[1] 
    lines = header.split('\r\n')
    if not lines:
        raise NetboaBadRequest('Empty Header.')
    line = lines.pop(0)
    items = line.split('\x20')
    if len(items) != 3:
        raise NetboaHttpBadRequest('Method line is not 3 arguments.')
    method = items[0]
    if method not in METHODS:
       raise NetboaHttpBadRequest('Unknown method: %s' % method) 
    req['method'] = method
    uri = items[1]
    if uri.startswith('/'):
        uri = uri[1:]
    req['uri'] = uri
    req['version'] = items[2]
    for line in lines:
        key, value = line.split(':\x20', 1)
        req[key.lower()] = value
    req['payload'] = payload.rstrip('\r\n')
    return req

def timestamp():
    """Return the date and time in RFC 1123 format."""
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%m:%S GMT')


