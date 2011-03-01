#------------------------------------------------------------------------------
#   netboa/telnet/telnet_eol_proto.py
#   Copyright Jim Storch 2010
#------------------------------------------------------------------------------

"""
Stream protocols for converting End-of-Lines between Python and Telnet.
"""

from netboa.coroutine import coroutine


_CR = '\r'          # Carriage Return or ASCII 10
_LF = '\n'          # Line Feed (Python newline) or ASCII 13
_NULL = '\x00'      # Null Character    


@coroutine
def to_telnet_eol(client, target):
    """
    Protocol to convert outward Python Line Feeds into Telnet compatible
    (Carriage Return + Line Feed) pairs.
    """    
    while True:
        byte = (yield)
        target.send(byte)
        if byte == _LF:
            next_byte = (yield)
            if next_byte != _CR:
                target.send(_CR)
            target.send(next_byte)


@coroutine
def from_telnet_eol(client, target):
    """
    Protocol to convert inward Telnet line terminators to Python-style
    newlines.

    Normally, Telnet lines are terminated with a CR-LF pair, however
    some application may use CR-NULL or just a LF so we need to cope
    with all three.
    """
    while True:
        byte = (yield)
        if byte == _CR:
            next_byte = (yield)
            if next_byte == _LF or next_byte == _NULL:
                target.send(_LF)
            else:
                ## weirdness, but not our place to argue
                target.send(_CR)
                target.send(next_byte)
        else:
            target.send(byte)

