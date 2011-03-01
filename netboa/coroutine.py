#------------------------------------------------------------------------------
#   netboa/coroutine.py
#   David Beazley's coroutine.py
#   See http://www.dabeaz.com/coroutines/  
#------------------------------------------------------------------------------

# A decorator function that takes care of starting a coroutine
# automatically on call.

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start

