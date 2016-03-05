"""
RAZE Python Libraries
Extensions to the standard logging module.

 * Loggable - Base class for objects that provide logging.

 * LoggableAdapter - Adapts regular objects to provide a loggable interface.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: logging_.py 369 2006-11-30 01:23:03Z james $
"""
__revision__ = "$Revision: 369 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/logging_.py $"
__all__ = [ 'Loggable' ]

from logging import *
from protocols import advise, AbstractBase


class Loggable(AbstractBase):
    """
    Base class for objects that provide logging.

    Initialize logging to log to stdout.

        >>> from sys import stdout
        >>> basicConfig(stream=stdout, level=DEBUG)

    Create a loggable class.

        >>> class MyLoggable(Loggable):
        ...    @property
        ...    def log_facility(self):
        ...      return 'raze.testing'
        ...
        ...    def format_log_message(self, message):
        ...      return message
        ...
        ...    def test_exception_logging(self):
        ...      try:
        ...        raise ValueError('test exception')
        ...      except:
        ...        self.log_exception()

        >>> obj = MyLoggable()

        >>> obj.log_debug('message')
        DEBUG:raze.testing:message

        >>> obj.log_info('message')
        INFO:raze.testing:message
    
        >>> obj.log_warning('message')
        WARNING:raze.testing:message

        >>> obj.log_error('message')
        ERROR:raze.testing:message

        >>> obj.log_critical('message')
        CRITICAL:raze.testing:message

        >>> obj.test_exception_logging()
        ERROR:raze.testing:None
        Traceback (most recent call last):
          File "<doctest raze.logging_.Loggable[2]>", line 11, in test_exception_logging
            raise ValueError('test exception')
        ValueError: test exception
    """
    @property
    def log_facility(self):
        """ 
        The facility to log messages to. This method is designed to be 
        overridden.
        """
        return type(self).__module__

    @property
    def logger(self):
        """ Retreive this objects logger. """
        return getLogger(self.log_facility)

    def format_log_message(self, message):
        """ Format the log message before logging it. """
        if message is None:
            return repr(self)
        return '%r: %s' % (self, message)

    def log_debug(self, *pos, **kw):
        """ Log a DEBUG message. """
        return self.log(DEBUG, *pos, **kw)

    def log_info(self, *pos, **kw):
        """ Log an INFO message. """
        return self.log(INFO, *pos, **kw)

    def log_warning(self, *pos, **kw):
        """ Log a WARNING message. """
        return self.log(WARNING, *pos, **kw)
    
    def log_error(self, *pos, **kw):
        """ Log an ERROR message. """
        return self.log(ERROR, *pos, **kw)
    
    def log_critical(self, *pos, **kw):
        """ Log a CRITICAL message. """
        return self.log(CRITICAL, *pos, **kw)
    
    def log_exception(self, level=ERROR, *pos, **kw):
        """ Log details of the current exception. """
        from sys import exc_info
        kw.setdefault('exc_info', exc_info())
        return self.log(level, message=None, *pos, **kw)

    def log(self, level, message, *pos, **kw):
        """ Log a message. """
        message = self.format_log_message(message)
        return self.logger.log(level, message, *pos, **kw)


class LoggableAdapter(Loggable):
    """ Adapts regular objects to provide a loggable interface. """
    advise(instancesProvide  = [ Loggable ],
           asAdapterForTypes = [ object ])

    def __init__(self, object):
        self.object = object

    @property
    def log_facility(self):
        """ The facility to log messages to. """
        class_ = type(self.object)
        return '%s.%s' % (class_.__module__, class_.__name__)


def _test():
    """ Test this module. """
    import doctest
    import logging_
    return doctest.testmod(logging_)
