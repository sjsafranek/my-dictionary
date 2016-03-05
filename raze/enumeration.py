"""
RAZE Python Libraries
Enumeration type.

 * Enumeration - Base class for user-defined enumeration types.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: enumeration.py 372 2006-11-30 03:49:23Z james $
"""
__revision__ = '$Revision: 372 $'
__location__ = '$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/enumeration.py $'
__all__ = [ 'Enumeration' ]


class MetaEnumeration(type):
    """ Enumeration meta class. """
    def __new__(metacls, name, bases, dict_):
        labels = dict_['labels']
        
        if isinstance(labels, dict):
            keys = sorted(labels.keys())
            dict_['labels'] = [ str(key) for key in keys ]
            dict_['values'] = [ int(labels[key]) for key in keys ]
        else:
            dict_['labels'] = [ str(key) for key in labels ]
            dict_['values'] = range(len(labels))

        return type.__new__(metacls, name, bases, dict_)

    def __init__(class_, name, bases, dict_):
        super(MetaEnumeration, class_).__init__(name, bases, dict_)
        # create the constants within the class
        for value, label in zip(class_.values, class_.labels):    
            setattr(class_, label, class_(label, value))

        # prevent sub-classing and further instantiations by replacing the __init__ method
        try:
            Enumeration
        except NameError:
            pass
        else:
            if class_ is not Enumeration:
                def noinit(self, *pos, **kw):
                    raise TypeError, 'cannot create custom instances of enum value'
                class_.__init__ = noinit

    def __iter__(class_):
        """ Iterate over the enum's values. """
        for label in class_.labels:
            yield getattr(class_, label)

    def __len__(class_):
        return len(class_.labels)

    def __getitem__(class_, key):
        if isinstance(key, basestring):
            return getattr(class_, key)
        elif isinstance(key, int):
            index = class_.values.index(key)
            return getattr(class_, class_.labels[index])
        else:
            raise TypeError, 'invalid key type: %s' % type(key).__name__

    def __str__(class_):
        return '%s(%s)' % (class_.__name__, ', '.join(class_.labels))

    def __repr__(class_):
        items = ', '.join([ '%s(%s)' % (label, value) for label, value in zip(class_.labels, class_.values) ])
        return "<enum '%s.%s' [%s]>" % (class_.__module__, class_.__name__, items)


class Enumeration(object):
    """
    Base class for user-defined enumeration types.

    Create a custom enumeration:

        >>> class FoodTypes(Enumeration):
        ...     labels = ('icecream', 'bread', 'yoghurt', 'dead_cow')
        
        >>> FoodTypes
        <enum 'raze.enumeration.FoodTypes' [icecream(0), bread(1), yoghurt(2), dead_cow(3)]>


    Access enumeration values as an attribute:
        
        >>> FoodTypes.yoghurt
        <constant yoghurt(2) of enum 'raze.enumeration.FoodTypes'>
        
        >>> print FoodTypes.icecream
        icecream
        
        >>> print FoodTypes.dead_cow.label
        dead_cow
        
        >>> print FoodTypes.dead_cow.value
        3


    Converting an enumeration value to an integer gives it's value.
        
        >>> int(FoodTypes.yoghurt) == FoodTypes.yoghurt.value
        True


    Enumeration types are iterable:
        
        >>> for item in FoodTypes:
        ...    print '%s = %s' % (item.label, item.value)
        icecream = 0
        bread = 1
        yoghurt = 2
        dead_cow = 3


    Enumeration types support random access by label and value.
        
        >>> FoodTypes['dead_cow']
        <constant dead_cow(3) of enum 'raze.enumeration.FoodTypes'>
        
        >>> FoodTypes[3]
        <constant dead_cow(3) of enum 'raze.enumeration.FoodTypes'>


    Enumeration values can be compared with other values of the same enumeration type.

        >>> if FoodTypes.icecream < FoodTypes.dead_cow:
        ...    print 'Steak is better!'
        Steak is better!


    Labels may also be mapped to non sequential values by using a dictionary.

        >>> class DictFoodTypes(Enumeration):
        ...     labels = { 'icecream' : 2, 'bread' : 18, 'dead_cow' : 23, 'steak' : 23 }
        
        >>> DictFoodTypes
        <enum 'raze.enumeration.DictFoodTypes' [bread(18), dead_cow(23), icecream(2), steak(23)]>


    Labels mapping to the same value compare as equal, but are still seperate instances.

        >>> DictFoodTypes.dead_cow == DictFoodTypes.steak
        True
        
        >>> DictFoodTypes.dead_cow is DictFoodTypes.steak
        False


    The __getitem__ operators continues to lookup by value, when there are multiple 
    labels with the same value, the first encountered is returned.

        >>> DictFoodTypes[23]
        <constant dead_cow(23) of enum 'raze.enumeration.DictFoodTypes'>
    """
    __metaclass__ = MetaEnumeration
    __slots__ = ('__label', '__value')
    labels = ()

    def __init__(self, label, value):
        super(Enumeration, self).__init__()
        self.__label = label
        self.__value = value

    @property
    def label(self):
        """ The label of this enum value. """
        return self.__label

    @property
    def value(self):
        """ Read-only access to the internal value. """
        return self.__value

    def __cmp__(self, other):
        """ Compare two enumeration values, must be values from the same enumeration type. """
        if type(self) is not type(other): 
            raise TypeError, 'can only compare enumerations of identical type'
        return cmp(self.value, other.value)

    def __getstate__(self):
        return self.__value, self.__label
    
    def __setstate__(self, value):
        self.__value, self.__label = value

    def __nonzero__(self):
        return bool(self.value)

    def __str__(self):
        return self.label

    def __int__(self):
        return self.value

    def __repr__(self):
        return "<constant %s(%s) of enum '%s.%s'>" % (self.label,
                                                      self.value,
                                                      self.__module__,
                                                      type(self).__name__)


def _test():
    """ Test this module. """
    import doctest
    import enumeration
    return doctest.testmod(enumeration)
