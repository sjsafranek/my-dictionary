"""
RAZE Python Libraries
Utilities for selecting the first "usable" value in a sequence.

 * CoalesceAttributes - Cascaded access of attributes on a seqeunce of 
                        namespaces.

 * coalesce - Return the first positional argument that is not None. If all 
              arguments are None, or no arguments are provided None is returned.

 * strict_coalesce - Return the first positional argument that is not None. If 
                     all arguments are None, or no arguments are provided a 
                     ValueError is raised.

 * coalesce_exceptions - Return the result of the first callable in a given 
                         sequence that does not raise a given set of exceptions.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: coalesce.py 363 2006-11-30 00:06:29Z james $
"""
__revision__ = "$Revision: 363 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/coalesce.py $"
__all__ = [ 'CoalesceAttributes', 'coalesce', 'strict_coalesce', 'coalesce_exceptions' ]


class CoalesceAttributes(object):
    """
    The CoalesceAttributes class allows cascaded access of attributes on a
    sequence of namespaces.

    Define some test objects to use as namespaces.

        >>> class Namespace1(object):
        ...   alpha = 'namespace1 - alpha'
        ...   gamma = 'namespace1 - gamma'

        >>> class Namespace2(object):
        ...   alpha = 'namespace2 - alpha'
        ...   beta  = 'namespace2 - beta'

        >>> class Namespace3(object):
        ...   delta = 'namespace3 - delta'


        >>> ca = CoalesceAttributes(Namespace1, Namespace2, Namespace3)

    Namespaces are searched in the order given:        

        >>> ca.alpha
        'namespace1 - alpha'

        >>> ca.beta
        'namespace2 - beta'
        
        >>> ca.gamma
        'namespace1 - gamma'

        >>> ca.delta
        'namespace3 - delta'

    Deleting an attribute will perform the delete only of the first namespace 
    with an attribute of that name.

        >>> del ca.alpha
        >>> ca.alpha
        'namespace2 - alpha'

    Setting an attribute will always set the attribute on the first given 
    namespace.  If no namespaces are given an AttributeError is raised.

        >>> ca.beta = 'the new beta'
        >>> Namespace1.beta is ca.beta
        True

        >>> Namespace2.beta
        'namespace2 - beta'

        >>> ca.new_attr = 'new attribute'
        >>> Namespace1.new_attr is ca.new_attr
        True

    When an attribute error can not be found in any of the given namespaces an 
    AttributeError is raised.

        >>> ca.not_found
        Traceback (most recent call last):
        AttributeError: not_found

    The namespace in which a given attribute exists can be obtained by using the 
    find_namespace() method.

        >>> ns = ca.find_namespace('delta')
        >>> ns is Namespace3
        True
    """
    def __init__(self, *namespaces):
        object.__setattr__(self, '_namespaces', namespaces)

    def find_namespace(self, name):
        for ns in self._namespaces:
            if hasattr(ns, name):
                return ns
        raise AttributeError(name)

    def __getattr__(self, name):
        ns = self.find_namespace(name)
        return getattr(ns, name)

    def __setattr__(self, name, value):
        try:
            ns = self._namespaces[0]
            setattr(ns, name, value)
        except IndexError:
            raise AttributeError(name)

    def __delattr__(self, name):
        ns = self.find_namespace(name)
        delattr(ns, name)


def coalesce(*pos):
    """
    Return the first positional argument that is not None. If all arguments are 
    None, or no arguments are provided None is returned.

        >>> coalesce(None, None, 46, 2)
        46

        >>> coalesce(None, None) is None
        True

        >>> coalesce() is None
        True
    """
    for value in pos:
        if value is not None:
            return value
    return None


def strict_coalesce(*pos):
    """
    Return the first positional argument that is not None. If all arguments are 
    None, or no arguments are provided a ValueError is raised.

        >>> strict_coalesce(None, None, 46, 2)
        46

        >>> strict_coalesce(None, None)
        Traceback (most recent call last):
        ValueError: strict coalesce failed

        >>> strict_coalesce()
        Traceback (most recent call last):
        ValueError: strict coalesce failed
    """
    value = coalesce(*pos)
    if value is None:
        raise ValueError('strict coalesce failed')
    return value


def coalesce_exceptions(exception, *callables):
    """
    Try to return the result of each callable in the callables list, moving on 
    to the next if an exception of the given type is raised. If all of the given 
    callables raise the given exception type, the exception is allowed to 
    propogate to the caller.

        >>> def func1():
        ...   raise ValueError

        >>> def func2():
        ...   raise RuntimeError

        >>> def func3():
        ...   return 'returned!'

    When an exception is raised that is not of the type specified, it is allowed 
    to propogate to the caller.

        >>> coalesce_exceptions(ValueError, func1, func2, func3)
        Traceback (most recent call last):
        RuntimeError

    Multiple exception types can be used by passing a tuple of exception types.

        >>> coalesce_exceptions((ValueError, RuntimeError), func1, func2, func3)
        'returned!'

    If none of the given callables return successfuly, the exception is allowed 
    to propogate to the caller.

        >>> coalesce_exceptions((ValueError, RuntimeError), func1, func2)
        Traceback (most recent call last):
        RuntimeError
    """
    for callable in callables:
        try:
            return callable()
        except exception:
            pass
    raise


def _test():
    """ Test this module. """
    import doctest
    import coalesce
    return doctest.testmod(coalesce)
