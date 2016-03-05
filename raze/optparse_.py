"""
RAZE Python Libraries
Extensions to the standard threading library.

 * OptionParser - Free-form option parser.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: optparse_.py 507 2006-12-14 05:04:03Z system $
"""
__revision__ = "$Revision: 507 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/optparse_.py $"
__all__ = [ 'OptionParser' ]

from re import compile
from sys import argv
from property_ import cached_property


class Option(object):
    """ A parsed option. """
    def __init__(self, name, *arguments):
        self.name      = name
        self.arguments = list(arguments)

    @property
    def value(self):
        if not self.arguments:
            return None
        return ' '.join(self.arguments)

    def __repr__(self):
        return '%s(%r, %r)' % (type(self).__name__, self.name, self.arguments)


class OptionParser(object):
    """
    Free-form command-line option parser.

        >>> arguments = 'foo bar --spam spam1 spam2 spam3 --d d1 d2'.split()
        >>> options = OptionParser(arguments)

    The arguments passed directly to the script are available via the arguments attribute.

        >>> options.arguments
        ['foo', 'bar']

    Options may be accessed directly as attributes.

        >>> options.spam
        Option('spam', ['spam1', 'spam2', 'spam3'])

        >>> options.d
        Option('d', ['d1', 'd2'])

        >>> options.spam.name
        'spam'

        >>> options.spam.value
        'spam1 spam2 spam3'

        >>> options.spam.arguments
        ['spam1', 'spam2', 'spam3']

    A list of all options is available via the options attribute:
        
        >>> options.options
        [Option('spam', ['spam1', 'spam2', 'spam3']), Option('d', ['d1', 'd2'])]
    """
    long  = compile('^\-\-([a-zA-Z0-9\-\_]+)$')
    short = compile('^\-([a-zA-Z0-9])$')
    
    def __init__(self, arguments=argv[1:]):
        self.raw_arguments = arguments
        self.arguments = []
        self.options   = []
        self._parse()
    
    def _parse(self):
        """ Parse the input attributes. """
        for chunk in self.raw_arguments:
            match = self.long.match(chunk) or self.short.match(chunk)
            if match:
                name = match.group(1)
                opt  = Option(name)
                self.options.append(opt)
            elif self.options:
                self.options[-1].arguments.append(chunk)
            else:
                self.arguments.append(chunk)

    @cached_property
    def dict(self):
        """ Dictionary mapping option name to option object. """
        return dict((o.name, o) for o in self.options)

    def __getattr__(self, name):
        try:
            return self.dict[name]
        except KeyError:
            raise AttributeError(name)


def _test():
    """ Test this module. """
    import doctest
    import optparse_
    return doctest.testmod(optparse_)
