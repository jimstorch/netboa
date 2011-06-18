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


METHODS = (b'HEAD', b'GET', b'POST', b'PUT', b'DELETE', b'TRACE', b'OPTIONS', 
    b'CONNECT', b'PATCH')

CONTENT_TYPES = {
    b'.html':b'text/html',
    b'.htm':b'text/html',
    b'.css':b'text/css',
    b'.txt':b'text/plain',
    b'.js':b'text/javascript',
    b'.png':b'image/png',
    b'.jpg':b'image/jpeg',
    b'.gif':b'image/gif',
    b'.svg':b'image/svg+xml',
    b'.svgz':b'image/svg+xml\r\nContent-Encoding: gzip',  ## omg hack
    b'.ico':b'image/x-icon',
    b'.pdf':b'application/pdf',
    }

def get_content_type(filename):
    foo, extension = os.path.splitext(filename)
    return CONTENT_TYPES.get(extension.lower(), b'application/x-unknown')

def parse_request(request):
    req = {}
    segments = request.split(b'\r\n\r\n', 1)
    if len(segments) != 2:
        raise NetboaHttpBadRequest(b'Missing header or terminator.') 
    header = segments[0]
    payload = segments[1] 
    lines = header.split(b'\r\n')
    if not lines:
        raise NetboaBadRequest(b'Empty Header.')
    line = lines.pop(0)
    items = line.split(b'\x20')
    if len(items) != 3:
        raise NetboaHttpBadRequest(b'Method line is not 3 arguments.')
    method = items[0]
    if method not in METHODS:
       raise NetboaHttpBadRequest(b'Unknown method: ' + method) 
    req['method'] = method
    req['uri'] = items[1].lstrip(b'/')
    req['version'] = items[2]
    for line in lines:
        items = line.split(b':\x20', 1)
        if len(items) != 2:
            raise NetboaHttpBadRequest(b'Malformed header parameter.')        
        key, value = items
        req[key.lower()] = value
    req['payload'] = payload.rstrip(b'\r\n')
    return req

def timestamp():
    """Return the date and time in RFC 1123 format."""
    return datetime.datetime.utcnow().strftime(
        '%a, %d %b %Y %H:%m:%S GMT').encode()

def respond_200(client, content_type, filename, content_length):
    response = b''.join((
        b'HTTP/1.0 200 OK\r\n',
        b'Date: ', timestamp(), b'\r\n',
        b'Content-Type: ', content_type, b'\r\n',
        b'Content-Disposition: filename="', filename, b'"\r\n',
        b'Content-Length: ', str(content_length).encode(), b'\r\n',
        b'Connection: close\r\n\r\n'
        ))
    client.send(response)

def respond_400(client, error):
    response = b''.join((
        b'HTTP/1.1 400 Bad Request\r\n',
        b'Date: ', timestamp(), b'\r\n',
        b'Connection: close\r\n',
        b'\r\n',
        b'<html><head><title>400 Bad Request</title></head>\r\n',
        b'<body>\r\n',
        b'<h1>Bad Request</h1>\r\n'
        b'<p>', error, b'</p>\r\n'
        b'</body></html>\r\n'
        ))        
    client.send(response)

def respond_404(client):
    response = b''.join((
        b'HTTP/1.1 404 Not Found\r\n',
        b'Date: ', timestamp(), b'\r\n',
        b'Connection: close\r\n\r\n',
        b'<html><head><title>404 Not Found</title></head>\r\n',
        b'<body>\r\n',
        b'<h1>Not Found</h1>\r\n',
        b'<p>The requested resource was not found.</p>\r\n',
        b'</body></html>\r\n'
        ))        
    client.send(response)

def respond_501(client):
    response = b''.join((
        b'HTTP/1.1 501 Method Not Implemented\r\n',
        b'Date: ', timestamp(), b'\r\n',
        b'Connection: close\r\n\r\n',
        b'<html><head><title>501 Method Not Implemented</title></head>\r\n',
        b'<body>\r\n',
        b'<h1>Method Not Implemented</h1>\r\n',
        b'</body></html>\r\n'
        ))
    client.send(response)

def respond_503(client):
    response =  b''.join((
        b'HTTP/1.1 503 Service Temporarily Unavailable\n',
        b'Date: ', timestamp(), b'\r\n',
        b'Connection: close\r\n\r\n',
        b'<html>\r\n',
        b'<head><title>503 Service Temporarily Unavailable</title></head>\r\n',
        b'<body>\r\n',
        b'<h1>Service Temporarily Unavailable</h1>\r\n',
        b'<p>The server is down for maintenance. Please try again later.\r\n',
        b'</p>\r\n',
        b'</body></html>\r\n'
        ))
    client.send(response)

