#!/usr/bin/env python
#------------------------------------------------------------------------------
#   netboa/websocket/sanity_check.py
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

"""
Wrote this to test that I'm correctly generating the responses for draft76
websockets.
"""

import struct
import hashlib


## From the draft76 docs:

REQUEST1 = (
    'GET /demo HTTP/1.1\r\n'
    'Host: example.com\r\n'
    'Connection: Upgrade\r\n'
    'Sec-WebSocket-Key2: 12998 5 Y3 1  .P00\r\n'
    'Sec-WebSocket-Protocol: sample\r\n'
    'Upgrade: WebSocket\r\n'
    'Sec-WebSocket-Key1: 4 @1  46546xW%0l 1 5\r\n'
    'Origin: http://example.com\r\n'
    '\r\n'
    '^n:ds[4U'
    )

CORRECT_RESPONSE1 = "8jKS'y:G*Co,Wxa-"

REQUEST2 = (
    'GET /demo HTTP/1.1\r\n'
    'Host: example.com\r\n'
    'Connection: Upgrade\r\n'
    'Sec-WebSocket-Key2: 1_ tx7X d  <  nw  334J702) 7]o}` 0\r\n'
    'Sec-WebSocket-Protocol: sample\r\n'
    'Upgrade: WebSocket\r\n'
    'Sec-WebSocket-Key1: 18x 6]8vM;54 *(5:  {   U1]8  z [  8\r\n'
    'Origin: http://example.com\r\n'
    '\r\n'
    'Tm[K T2u'
    )

CORRECT_RESPONSE2 = 'fQJ,fN/4F4!~K~MH'

def parse_request(request):
    req = {}
    segments = request.split('\r\n\r\n', 1)
    assert(len(segments) == 2)
    header, payload = segments
    lines = header.split('\r\n')
    line = lines.pop(0)
    items = line.split('\x20',2)
    assert(len(items) == 3)
    req['method'] = items[0]
    req['request_uri'] = items[1]
    req['http_version'] = items[2]
    for line in lines:
        parts = line.split(':\x20', 1)
        assert(len(parts) == 2)
        req[parts[0].lower()] = parts[1]
    req['payload'] = payload
    return req

def get_word(key):
    digits=''
    spaces=0
    for char in key:
        if char.isdigit():
            digits += char
        elif char == '\x20':
            spaces += 1
    assert(spaces)
    assert(digits)
    keynum = int(digits)
    assert(keynum % spaces == 0)
    wordval = keynum / spaces
    assert(wordval < 2 ** 32)
    return struct.pack("!I", wordval)

def create_token(req):
    key1 = req.get('sec-websocket-key1', None)
    assert(key1 is not None)
    word1 = get_word(key1)
    key2 = req.get('sec-websocket-key2', None)
    assert(key2 is not None)
    word2 = get_word(key2)
    salt = req.get('payload', None)
    assert(salt is not None)
    assert(len(salt)==8)
    return hashlib.md5(word1 + word2 + salt).digest()    

req = parse_request(REQUEST1)
print create_token(req) == CORRECT_RESPONSE1

req = parse_request(REQUEST2)
print create_token(req) == CORRECT_RESPONSE2

