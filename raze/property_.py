"""
Extensions to the standard property type.

 * cached_property - Property that caches the result of it's get function until 
                     either set or delete are called.
 
 * weakref_property - The WeakRefProperty class is an property that stores it's 
                      value as a weak reference.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: property_.py 545 2006-12-18 12:48:10Z james $
"""
__revision__ = "$Revision: 545 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/property_.py $"
__all__ = [ 'cached_property', 'weakref_property' ]

from weakref import WeakKeyDictionary, ref


class cached_property(property):
    """
    cached_property is an extension to the builtin property that caches the 
    result of the fget function. The cached value is cleared when either of the 
    fset or fdel functions are called.


        >>> class Foo(object):
        ...   def __init__(self):
        ...     self.value = 0
        ...
        ...   def resource_intensive_operation(self):
        ...     from raze.misc import SimpleObject
        ...     print 'Performing resource intensive operation.'
        ...     return SimpleObject(value=self.value)
        ...
        ...   def get_prop(self):
        ...     return self.resource_intensive_operation()
        ...
        ...   def set_prop(self, value):
        ...     self.value = value
        ...
        ...   prop = cached_property(get_prop, set_prop)

        >>> x = Foo()

    The first time the property is accessed, the get function is called:

        >>> first = x.prop
        Performing resource intensive operation.

    Subsequent property access uses the cached value:

        >>> second = x.prop
        >>> first is second
        True

        >>> first.value
        0

    Until either the property is either set or deleted, in this case the 
    property is set to 42, notice on the next fetch the 'resource intensive 
    operation' is performed again.

        >>> x.prop = 42

        >>> third = x.prop
        Performing resource intensive operation.

        >>> fourth = x.prop
        >>> third is fourth
        True
    """
    __slots__ = 'cache'

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        super(cached_property, self).__init__(fget, fset, fdel, doc)
        self.cache = WeakKeyDictionary()

    def __get__(self, instance, owner):
        try:
            return self.cache[instance]
        except KeyError:
            value = self.cache[instance] = super(cached_property, self).__get__(instance, owner)
            return value

    def __set__(self, instance, value):
        self.cache.pop(instance, None)
        super(cached_property, self).__set__(instance, value)
    
    def __delete__(self, instance):
        self.cache.pop(instance, None)
        super(cached_property, self).__delete__(instance)


class weakref_property(property):
    """
    weakref_property is a property helper that stores it's value as a weak reference.
    It differs from the other property types in that it does not allow you to 
    specify custom get/set methods.

        >>> class ReferencedObject(object):
        ...   pass

        >>> class Foo(object):
        ...   weak_prop = weakref_property('Test weakreference property.')

        >>> f = Foo()
        >>> f.weak_prop is None
        True

        >>> r = ReferencedObject()
        >>> f.weak_prop = r
        >>> f.weak_prop is r
        True

    When the last reference to the ReferencedObject instance ('r') is lost, the 
    object goes out of scope, and the weakref_property will give None.

        >>> del r
        >>> f.weak_prop is None
        True
    """
    __slots__ = 'references'

    def __init__(self, doc=None):
        self.references = WeakKeyDictionary()
        super(weakref_property, self).__init__(self.fget, self.fset, self.fdel, doc)

    def make_reference(self, value):
        """ Create a weak reference to the given value. """
        return ref(value)

    def fget(self, instance):
        """ Fetch the weak-referenced object. """
        try:
            return self.references[instance]()
        except KeyError:
            return None
    
    def fset(self, instance, value):
        """ Set the object that is to be weak-referenced. """
        self.references[instance] = self.make_reference(value)

    def fdel(self, instance):
        """ Remove the weak-reference. """
        self.references.pop(instance, None)


def _test():
    """ Test this module. """
    import doctest
    import property_
    return doctest.testmod(property_)
