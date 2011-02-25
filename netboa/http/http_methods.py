#------------------------------------------------------------------------------
#   netboa/http/http_methods.py
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

from netboa.http.http_lib import timestamp


def respond_200(client, content_type, filename, content_length):
    header = (
        'HTTP/1.0 200 OK\r\n'
        'Date: %s\r\n'
        'Content-Type: %s\r\n'
        'Content-Disposition: filename="%s"\r\n'
        'Content-Length: %d\r\n'
        'Connection: close\r\n'
        '\r\n'
        )
    response = header %(timestamp(), content_type, filename, content_length)
    client.send(response)

def respond_400(client, error):
    response = (
        'HTTP/1.1 400 Bad Request\r\n'
        'Date: %s\r\n'
        'Connection: close\r\n'
        '\r\n'
        '<html><head><title>400 Bad Request</title></head>\r\n'
        '<body>\r\n'
        '<h1>Bad Request</h1>\r\n'
        '<p>%s</p>\r\n'
        '</body></html>\r\n'
        )        
    client.send(response % (timestamp(), str(error)))

def respond_404(client):
    response = (
        'HTTP/1.1 404 Not Found\r\n'
        'Date: %s\r\n'
        'Connection: close\r\n'
        '\r\n'
        '<html><head><title>404 Not Found</title></head>\r\n'
        '<body>\r\n'
        '<h1>Not Found</h1>\r\n'
        '<p>The requested resource was not found.</p>\r\n'
        '</body></html>\r\n'
        )        
    client.send(response % timestamp())

def respond_501(client):
    response = (
        'HTTP/1.1 501 Method Not Implemented\r\n'
        'Date: %s\r\n'
        'Connection: close\r\n'
        '\r\n'
        '<html><head><title>501 Method Not Implemented</title></head>\r\n'
        '<body>\r\n'
        '<h1>Method Not Implemented</h1>\r\n'
        '</body></html>\r\n'
        )
    client.send(response % timestamp())

def respond_503(client):
    response =  (
        'HTTP/1.1 503 Service Temporarily Unavailable\n'
        'Date: %s\r\n'
        'Connection: close\r\n'
        '\r\n'
        '<html>\r\n'
        '<head><title>503 Service Temporarily Unavailable</title></head>\r\n'
        '<body>\r\n'
        '<h1>Service Temporarily Unavailable</h1>\r\n'
        '<p>The server is down for maintenance. Please try again later.\r\n'
        '</p>\r\n'
        '</body></html>\r\n'
        )
    client.send(response % timestamp())
