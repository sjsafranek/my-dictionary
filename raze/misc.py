"""
Miscellaneous helper/utility classes and functions. 

 * SimpleObject - Create an object on which you can new attributes.

 * Default - Global singleton to use as a default parameter (instead of None).

 * join - Replacement for str.join() which operates correctly on generators and 
          automatically converts sequence items to strings.

 * conditional - Loose emulation of the ternary operator (?:), this function 
                 will be deprecated when RAZE is retargeted to Python 2.5.

 * attribute_dict - Obtain a dictionary of attributes for a given object even if 
                    the object uses slots.
 
 * limit_str - Limit a string to the given length.

 * getattr_  - Replacement for getattr that allows use of dot-notation in 
               attribute names.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: misc.py 426 2006-12-04 05:41:26Z james $
"""
__revision__ = "$Revision: 426 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/misc.py $"
__all__ = [ 'SimpleObject', 'TruncatedString' , 'DefaultType', 'Default', 'join', 'conditional', 'attribute_dict', 'limit_str', 'getattr_' ]

from container import conform_list
from singleton import Singleton


class SimpleObject(object):
    """
    SimpleObject can be used to create simple objects which allow attribute 
    creation (unlike the 'object' class).

        >>> x = SimpleObject()
        >>> x.foo = 123
        >>> x.foo
        123

    Keyword parameters passed to SimpleObject's constructor become instance 
    attributes.

        >>> x = SimpleObject(bar=111)
        >>> x.bar
        111
    """
    def __init__(self, **kw):
        super(SimpleObject, self).__init__()
        self.__dict__.update(kw)


class DefaultType(Singleton):
    """
    Global singleton to use as a default parameter (instead of None).

        >>> def foo(arg=Default):
        ...   if arg is Default:
        ...     return 'used default'
        ...   return 'used argument'

        >>> foo()
        'used default'

        >>> foo(1)
        'used argument'

    The default object is designed to combat the situation where when None is 
    used as indicator that some other value is to be used as the default, but 
    the caller actually needs to use None as the value.
    """
    __slots__ = ()
    def __repr__(self):
        return '<Default>'
    def __str__(self):
        return '<Default>'

Default = DefaultType()


def join(sequence, separator=', ', format='%s'):
    """
    The join function provides a 'safe' implementation of the standard join. Before 
    joining, each element in the sequence is converted to a string using the given 
    format specifier.

        >>> sequence = [ 1, 2, 3 ]
        >>> join(sequence)
        '1, 2, 3'

        >>> join(sequence, separator='-')
        '1-2-3'

        >>> join(sequence, separator='-', format='(%s)')
        '(1)-(2)-(3)'

        >>> def generator():
        ...   yield 1
        ...   yield 2
        ...   yield 3

        >>> join(generator())
        '1, 2, 3'
    """
    strings = [format % element for element in sequence]
    return separator.join(strings)


def conditional(condition, true_value, false_value):
    """
    Loose emulation of the ternary operator (?:). Returns true_value if 
    condition is True, otherwise returns false_value.

    Note that this function differs from the ternary operator in that the unused 
    value is not shortcircuited.

        >>> conditional(True, 1, 2)
        1

        >>> conditional(False, 1, 2)
        2
    """
    if condition:
        return true_value
    return false_value


def attribute_dict(obj, default={}):
    """
    Return a dictionary of an object's attributes, even if the object uses slots.
    If there is no way to determine how to obtain the object's attributes, the 
    value of default is returned (defaults to an empty dictionary).

        >>> obj = object()
        >>> attribute_dict(obj) 
        {}

        >>> attribute_dict(obj, None) is None
        True


        >>> class UsesSlots(object):
        ...   __slots__ = ('a', 'b', 'c')
        ...   def __init__(self):
        ...     self.a = 100

        >>> obj = UsesSlots()
        >>> attribute_dict(obj)
        {'a': 100}
    """
    if hasattr(obj, '__dict__'):
        return dict(obj.__dict__)
    if hasattr(obj, '__slots__'):
        slots = conform_list(obj.__slots__)
        pairs = [ (name, getattr(obj, name)) for name in slots if hasattr(obj, name) ]
        return dict(pairs)
    return default


def limit_str(input, limit, indicator='...'):
    """
    Limit input string to the given length.

    Note that the truncation indicator ('...' by default) is included in length calculations:

        >>> limit_str('Hello, world!', 10)
        'Hello, ...'

    An alternative truncation indicator may be specified:

        >>> limit_str('Hello, world!', 10, '*')
        'Hello, wo*'
    """
    if len(input) <= limit:
        return input
    if indicator is None:
        return input[:limit]
    return input[:limit - len(indicator)] + indicator


def getattr_(obj, name, default=Default):
    """
    Replacement for getattr that allows use of dot-notation in attribute names.

        >>> x = SimpleObject()
        >>> x.y = SimpleObject()
        >>> x.y.z = SimpleObject()

        >>> getattr_(x, 'y') is x.y
        True

        >>> getattr_(x, 'y.z') is x.y.z
        True

        >>> getattr_(x, 'missing', None) is None
        True

        >>> getattr_(x, 'missing')
        Traceback (most recent call last):
        AttributeError: 'SimpleObject' object has no attribute 'missing'
    """
    try:
        for n in name.split('.'):
            obj = getattr(obj, n)
        return obj
    except AttributeError:
        if default is Default:
            raise
        return default


def _test():
    """ Test this module. """
    import doctest
    import misc
    return doctest.testmod(misc)
