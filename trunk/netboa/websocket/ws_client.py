#------------------------------------------------------------------------------
#   netboa/websocket/ws_client.py
#   Copyright 2012 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#------------------------------------------------------------------------------


import struct
import array 

from netboa import verbosity
from netboa import str_to_bytes
from netboa import bytes_to_str
from netboa.client import Client
from netboa.websocket.ws_error import NetboaWsBadFrame
from netboa.websocket.ws_error import NetboaWsCloseFrame

def unpack_frame(data):
    size = len(data)
    if size < 1:
        raise NetboaWsBadFrame('[WS13] empty frame.')
    #if l < 
    byte1, byte2 = struct.unpack_from('!BB', data)
    if not (byte1 >> 7) & 1:
        raise NetboaWsBadFrame('[WS13] final bit not set.')
    opcode = byte1 & 0xf
    ## Firefox sends a close-frame opcode when you close the page
    if opcode & 0x8:
        raise NetboaWsCloseFrame('[WS13] close-frame opcode received.') 
    if not opcode & 0x1:
        raise NetboaWsBadFrame('[WS13] not text frame.') 
    masked = (byte2 >> 7) & 1
    mask_offset = 4 if masked else 0
    payload_hint = byte2 & 0x7f
    if payload_hint < 126:
        payload_offset = 2
        payload_length = payload_hint
    elif payload_hint == 126:
        payload_offset = 4
        if size < 4:
            raise NetboaWsBadFrame('[WS13] too short for 16b payload length.')  
        payload_length = struct.unpack_from('!H',data,2)[0]
    elif payload_hint == 127:
        payload_offset = 8
        if size < 8:
            raise NetboaWsBadFrame('[WS13] too short for 64b payload length.')  
        payload_length = struct.unpack_from('!Q',data,2)[0]
    payload = array.array('B')
    payload.fromstring(data[payload_offset + mask_offset:])
    if len(payload) != payload_length:
        raise NetboaWsBadFrame('[WS13] malformed payload length.')      
    if masked:
        if size < (payload_offset + 4):
            raise NetboaWsBadFrame('[WS13] frame too short for mask.')    
        mask_bytes = struct.unpack_from('!BBBB',data,payload_offset)
        for i in range(len(payload)):
            payload[i] ^= mask_bytes[i % 4]
    return payload.tostring()


def pack_frame(payload):
    header = b'\x81'        # Final Frame Flag & Text Frame Op Code
    size = len(payload)
    if size < 126:
        header += struct.pack('!B', size)
    elif size < 2**16:
        header += struct.pack('!BH', 126, size)
    elif size < 2**64:
        header += struct.pack('!BQ', 127, size)
    else:
        raise BaseException('[WS13] WTF are you trying to send?') 
    return header + payload


class WsClient(Client):
    
    def __init__(self, sock, address, port):
        Client.__init__(self, sock, address, port)

    def get_string(self):
        data = bytes_to_str(self.get_bytes())
        try:
			payload = unpack_frame(data)
        except NetboaWsCloseFrame as error:
            payload = ''
            self.server.vprint('[WebSocket] %s' % error, verbosity.INFO)
            self.deactivate()
        except NetboaWsBadFrame as error:
            payload = ''
            self.server.vprint('[WebSocket Error] %s' % error, verbosity.ERROR)
            self.deactivate()
        return payload
    
    def send(self, data):
        frame = pack_frame(data)
        self.send_raw(frame)
       
    def send_raw(self, data):
        if type(data) == str:
            self.send_buffer += str_to_bytes(data)
        else:
            self.send_buffer += data
        self.server._request_send(self)
