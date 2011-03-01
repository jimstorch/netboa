#------------------------------------------------------------------------------
#   netboa/telnet/telnet_iac_proto.py
#   Copyright Jim Storch 2010
#------------------------------------------------------------------------------

"""
Stream protocol for processing Telnet 'Interpret as Command' (IAC) sequences.
"""


from netboa.coroutine import coroutine
from netboa.telnet.telnet_codes import *
from netboa.telnet.telnet_options import *


@coroutine
def send_sink(client):
    while True:
        byte = (yield)
        #print byte, 
        client.send_buffer += byte

@coroutine
def recv_sink(client):
    while True:
        byte = (yield)
        #print byte, 
        client.recv_buffer += byte

#            if cmd == SB:
#                sb = ''
#                while True:
#                    data = (yield)
#                    if data == SE: break
#                    else: sb += data
#                ## process SB
#            else:
#                ## incorrect sequence
#                pass                


@coroutine
def telnet_iac(client, target):

    while True:
        byte = (yield)

        if byte == IAC:
            cmd = (yield)

            ## Process Two-Byte Commands

            if cmd == NOP:
                pass

            elif cmd == DATMK:
                pass

            elif cmd == IP:
                pass

            elif cmd == AO:
                pass

            elif cmd == AYT:
                pass

            elif cmd == EC:
                pass

            elif cmd == EL:
                pass

            elif cmd == GA:
                pass

            ## Process Three-Byte Commands

            elif cmd == DO:
                option = (yield)

                if option == BINARY:
                    if check_reply_pending(client, BINARY):
                        note_reply_pending(client, BINARY, False)
                        note_local_option(client, BINARY, True)
                    elif (check_local_option(client, BINARY) is False or
                            check_local_option(client, BINARY) is UNKNOWN):
                        note_local_option(client, BINARY, True)
                        iac_will(client, BINARY)

                elif option == ECHO:
                if check_reply_pending(client, ECHO):
                    note_reply_pending(client, ECHO, False)
                    note_local_option(client, ECHO, True)

                elif (check_local_option(client, ECHO) is False or
                        check_local_option(client, ECHO) is UNKNOWN):
                    note_local_option(client, ECHO, True)
                    iac_will(client, ECHO)
                    client.event('telnet_echo', True)
                                        

            elif cmd == DONT:
                option = (yield)

            elif cmd == WILL:
                option = (yield)

            elif cmd == WONT:
                option = (yield)

            else:
                ## incorrect sequence, forward to client
                target.send(cmd)
        
        else:
            ## forward non-telnet to client
            target.send(byte)
