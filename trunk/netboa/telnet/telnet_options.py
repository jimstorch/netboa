#------------------------------------------------------------------------------
#   netboa/telnet/telnet_options.py
#   Copyright Jim Storch 2010
#------------------------------------------------------------------------------

from netboa.telnet.telnet_codes import *

#   We need to track up to 256 Telnet Options.
#   Each option has a local and remote state, plus we need to know if we're
#   expecting a reply.
#   So we'll use a three field array:
#       0 = local state; True, False, or UNKNOWN
#       1 = remote state; True, False, or UNKNOWN
#       2 = reply pending, True or False
#
#   We'll store these in the client 'meta' dictionary by option value


def check_local_option(client, option):
    options = client.get_property(option)
    if options is None:
        return UNKNOWN
    else:
        return options[0]

def note_local_option(client, option, state):
    options = client.get_property(option)
    if options is None:
        client.set_property(options, [state, UNKNOWN, False])    
    else:
        options[0] = state
        client.set_property(option, options)

def check_remote_option(client, option):
    options = client.get_property(option)
    if options is None:
        return UNKNOWN
    else:
        return options[1]

def note_remote_option(client, option, state):
    options = client.get_property(option)
    if options is None:
        client.set_property(options, [UNKNOWN, state, False])    
    else:
        options[1] = state
        client.set_property(option, options)

def check_reply_pending(client, option):
    options = client.get_property(option)
    if options is None:
        return False
    else:
        return options[2]

def note_reply_pending(client, option, state):
    options = client.get_property(option)
    if options is None:
        client.set_property(options, [UNKNOWN, UNKNOWN, state])    
    else:
        options[2] = state
        client.set_property(option, options)

def iac_do(client, option):
    client.send('%c%c%c' % (IAC, DO, option))

def iac_dont(client, option):
    client.send('%c%c%c' % (IAC, DONT, option))

def iac_will(client, option):
    client.send('%c%c%c' % (IAC, WILL, option))

def iac_wont(client, option):
    client.send('%c%c%c' % (IAC, WONT, option))

