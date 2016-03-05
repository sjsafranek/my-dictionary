"""
RAZE Python Libraries
Extensions to the standard threading library.

 * SimpleCondition - Provides a simpler interface to a Condition object.

 * exclusive - Decorator that locks a mutex (RLock object) when the decorated 
               function is called, and releases it after the function exits.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: threading_.py 371 2006-11-30 01:33:13Z james $
"""
__revision__ = "$Revision: 371 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/threading_.py $"
__all__ = [ 'SimpleCondition', 'exclusive' ]


try:
    from threading import *
    import threading as threading_lib
except ImportError:
    from dummy_threading import *
    import dummy_threading as threading_lib

__all__ += threading_lib.__all__


class SimpleCondition(object):
    """ Provides a simpler interface to a Condition object. """
    __slots__ = 'condition'

    def __init__(self, condition=None):
        self.condition = condition or Condition()
    
    def wait(self, timeout=None):
        """ Acquire the condition, wait for a notify then release. """
        self.condition.acquire()
        try:
            self.condition.wait(timeout)
        finally:
            self.condition.release()
    
    def notify(self):
        """ Acquire the condition, notify a waiting thread then release. """
        self.condition.acquire()
        try:
            self.condition.notify()
        finally:
            self.condition.release()

    def notify_all(self):
        """ Acquire the condition, notify all waiting thread then release. """
        self.condition.acquire()
        try:
            self.condition.notifyAll()
        finally:
            self.condition.release()


def exclusive(func):
    """
    Decorator that locks a mutex around calls.

        >>> @exclusive
        ... def my_exclusive_func():
        ...   return 'exclusive access!'
       
        >>> my_exclusive_func.__name__
        'my_exclusive_func'

    No two-threads can call an exclusive function at the same time, any thread 
    that attempts to call the exclusive function while it is already executing 
    blocks until execution is complete.

        >>> my_exclusive_func()
        'exclusive access!'
    """
    mutex = RLock()
    def invoker(*pos, **kw):
        try:
            mutex.acquire()
            return func(*pos, **kw)
        finally:
            mutex.release()
    invoker.__name__ = func.__name__
    invoker.__doc__  = func.__doc__
    return invoker


def _test():
    """ Test this module. """
    import doctest
    import threading_
    return doctest.testmod(threading_)
