#------------------------------------------------------------------------------
#   netboa/websocket/handshake76.py
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
*******************
THIS FILE IS BROKEN
*******************

I started writing this handshake because it's the one detailed in the current
draft of the WebSocket spec.  But when I went to test it, I found that Chromium
was sending the upgrade request using the previous format.

So, maybe I'll need this. 
"""

#import struct
#import hashlib

#from netboa.websocket.ws_error import NetboaWsBadRequest


#RESPONSE76 = (
#    'HTTP/1.1 101 WebSocket Protocol Handshake\r\n'
#    'Upgrade: WebSocket\r\n'
#    'Connection: Upgrade\r\n'
#    'Sec-WebSocket-Origin: %s\r\n'
#    'Sec-WebSocket-Location: %s:%d\r\n'
#    '\r\n'
#    '%s\r\n'
#    )

#def handshake76(client, req):
#    key1 = req.get('sec-websocket-key1', False)
#    key2 = req.get('sec-websocket-key2', False)
#    msg = req.get('message', False)
#    origin = req.get('origin', False)
#    if not key1 or not key2 or not msg or not orgin:
#        raise NetboaWsBadRequest('Missing WebSocket Keys.')  
#    spaces1 = spaces2 =0
#    digits1 = digits2 = ''
#    for ch in key1:
#        if ch == '\x20':
#            spaces1 +=1
#        elif ch.isdigit():
#            digits1 += ch
#    for ch in key2:
#        if ch == '\x20':
#            spaces2 +=1
#        elif ch.isdigit():
#            digits2 += ch
#    try:
#        val1 = int(digits1) / spaces1
#        val2 = int(digits2) / spaces2
#    except ValueError, ZeroDivisionError:
#        raise NetboaWsBadRequest('Malformed WebSocket Keys')     
#    handshake = struct.pack('!I', val1) + struct.pack('!I', val2) + msg
#    key_phrase = hashlib.md5(handshake).digest()
#    key_phrase = decode76(req)
#    response = RESPONSE76 % (origin, origin, client.ws_port, key_phrase)
#    print response
#    client.send(response) 
    
    
