"""
RAZE Python Libraries
Convert identifier names between different naming conventions.

 * NameStyle - Enumeration of different identity naming styles.

 * NameStyleConverter - Class for converting identifiers to different styles.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: namestyle.py 372 2006-11-30 03:49:23Z james $
"""
__revision__ = "$Revision: 372 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/namestyle.py $"
__all__ = [ 'NameStyle', 'NameStyleConverter' ]

from re import compile
from string import ascii_lowercase
from enumeration import Enumeration
from raze.misc import join


class NameStyle(Enumeration):
    """
    Enumeration of naming styles.

    lower  ->  lower_case_seperated_by_underscores
    upper  ->  UPPER_CASE_SEPERATED_BY_UNDERSCORES
    camel  ->  CamelCase aka WordsRunTogether
    mixed  ->  javaStyleFunctionName

    The NameStyle enumeration can identify which style an identifier is using.

        >>> NameStyle.identify('foo_bar')
        <constant lower(0) of enum 'raze.namestyle.NameStyle'>

        >>> NameStyle.identify('FOO_BAR')
        <constant upper(1) of enum 'raze.namestyle.NameStyle'>

        >>> NameStyle.identify('FooBar')
        <constant camel(2) of enum 'raze.namestyle.NameStyle'>

        >>> NameStyle.identify('fooBar')
        <constant mixed(3) of enum 'raze.namestyle.NameStyle'>
    """
    labels = [ 'lower', 'upper', 'camel', 'mixed' ]

    @classmethod
    def is_lower(class_, identifier):
        """ Return true if identifier uses the 'lower' naming style. """
        regex = compile('^[a-z\_][a-z0-9\_]*$')
        return regex.match(identifier)

    @classmethod
    def is_upper(class_, identifier):
        """ Return true if identifier uses the 'upper' naming style. """
        regex = compile('^[A-Z\_][A-Z0-9\_]*$')
        return regex.match(identifier)

    @classmethod
    def is_camel(class_, identifier):
        """ Return true if identifier uses the 'camel' naming style. """
        regex = compile('^([A-Z]+[a-z0-9]*)*[\_]*$')
        if regex.match(identifier):
            return True
        regex = compile('^[\_]+[0-9]*([A-Z]+[a-z0-9]*)*[\_]*$')
        return regex.match(identifier)

    @classmethod
    def is_mixed(class_, identifier):
        """ Return true if identifier uses the 'mixed' naming style. """
        regex = compile('^[a-z][a-z0-9]*([A-Z]+[a-z0-9]*)+[\_]*$')
        if regex.match(identifier):
            return True
        regex = compile('^[\_]+[0-9]*[a-z]+([A-Z]+[a-z0-9]*)*[\_]*$')
        return regex.match(identifier)

    @classmethod
    def identify(class_, identifier):
        """ Identify the naming style used by identifier, returning a NameStyle constant. """
        for constant in class_:
            if getattr(class_, 'is_%s' % constant.label)(identifier):
                return constant
        raise ValueError('Could not identify style of: "%s".' % identifier)



class NameStyleConverter(object):
    """
    Identifiers and parses an identifier. The identifier can then be converted 
    to different styles.

    The NameStyleConverter class identifies the name style used, parses the input, 
    then allows you to convert the identifier to any other naming style.

        >>> converter = NameStyleConverter('___foo_bar__')
        >>> converter.lower
        '___foo_bar__'

        >>> converter.upper
        '___FOO_BAR__'

        >>> converter.camel
        '___FooBar__'

        >>> converter.mixed
        '___fooBar__'


    NameStyleConverters are comparable.

        >>> nsc1 = NameStyleConverter('foo_bar')
        >>> nsc2 = NameStyleConverter('fooBar')
        >>> nsc1 == nsc2
        True

        >>> nsc3 = NameStyleConverter('zzz')
        >>> nsc1 == nsc3
        False

        >>> nsc1 < nsc3
        True


    Converters may be joined (operator+ is an alias for join).

        >>> nsc4 = nsc1 + nsc3
        >>> nsc4.camel
        'FooBarZzz'


    Now for the sake of testing, let's try parsing each style.
        
        >>> results = set()
        >>> for constant in NameStyle:
        ...   identifier = getattr(converter, constant.label)
        ...   nsc = NameStyleConverter(identifier)
        ...   results.add(nsc.lower)

        >>> results
        set(['___foo_bar__'])


    Please note that the current version of NameStyleConverter does not support 
    identifiers with digits.

        >>> NameStyleConverter('foo34')
        Traceback (most recent call last):
        NotImplementedError: Identifiers containing digits are not supported at this time.
    """
    def __init__(self, identifier, style_hint=None):
        """ If the style can not be determined it is assumed to be 'style_hint'. """

        if compile('[0-9]').search(identifier):
            raise NotImplementedError('Identifiers containing digits are not supported at this time.')
        
        try:
            self._input_style = NameStyle.identify(identifier)
        except ValueError:
            if style_hint is None:
                raise
            self._input_style = style_hint
        self._input = identifier
        self._chunks = self._parse()

    @property
    def leading_underscores(self):
        """ The number of leading underscores present in the input identifier. """
        for count, char in enumerate(self._input):
            if char != '_': break
        return '_' * count

    @property
    def trailing_underscores(self):
        """ The number of leading underscores present in the input identifier. """
        for count, char in enumerate(reversed(self._input)):
            if char != '_': break
        return '_' * count

    @property
    def _center(self):
        ll = len(self.leading_underscores)
        tl = len(self.trailing_underscores)
        il = len(self._input)
        return self._input[ll:il-tl]

    @property
    def lower(self):
        """ Convert the identifier to 'lower' naming style. """
        return self.leading_underscores + join((chunk.lower() for chunk in self._chunks), '_') + self.trailing_underscores
        
    @property
    def upper(self):
        """ Convert the identifier to 'upper' naming style. """
        return self.leading_underscores + join((chunk.upper() for chunk in self._chunks), '_') + self.trailing_underscores

    @property
    def camel(self):
        """ Convert the identifier to 'camel' naming style. """
        return self.leading_underscores + join((chunk.title() for chunk in self._chunks), '') + self.trailing_underscores

    @property
    def mixed(self):
        """ Convert the identifier to 'mixed' naming style. """
        front = [ chunk.lower() for chunk in self._chunks[:1] ]
        back  = [ chunk.title() for chunk in self._chunks[1:] ]
        return self.leading_underscores + join(front + back, '') + self.trailing_underscores

    def _parse_lower(self):
        return self._center.split('_')

    def _parse_upper(self):
        return self._parse_lower()

    def _parse_camel(self):
        regex = compile('[A-Z][a-z]+')
        return regex.findall(self._center)
    
    def _parse_mixed(self):
        for count, char in enumerate(self._center):
            if char not in ascii_lowercase: break
        regex = compile('[A-Z][a-z]+')
        return [ self._center[:count] ] + regex.findall(self._center[count:])

    def _parse(self):
        method = getattr(self, '_parse_%s' % self._input_style.label)
        return [ chunk.lower() for chunk in method() ]

    def join(self, other):
        """ Create a new NameStyleConverter by appending other to self. """
        if not isinstance(other, NameStyleConverter):
            other = NameStyleConverter(other)
        return NameStyleConverter(self.lower + '_' + other.lower)
    
    def __add__(self, other):
        return self.join(other)

    def __cmp__(self, other):
        if hasattr(other, '_chunks'):
            return cmp(self._chunks, other._chunks)
        return super(NameStyleConverter, self).__cmp__(other)


def _test():
    """ Test this module. """
    import doctest
    import namestyle
    return doctest.testmod(namestyle)
