"""
RAZE Python Libraries
Extended container types and utilities.

 * BidirectionalDictionary - Dictionary that maintains key -> value 
                             relationships in both directions.

 * merge_dictionary - Create a new dictionary with all elements from the given 
                      dictionaries.

 * invert_dictionary - Return the 'inverse' of the given dictionary (values 
                       become keys).

 * xzip - Like zip(), but instead of returning a list, returns an object that 
          generates the zipped sequence on demand.

 * xenumerate - Like enumerate(), but instead of returning a list, returns an 
                object that generates the enumerated sequence in demand.

 * even_elements - Yield only the even elements of a sequence.

 * odd_elements - Yield only the odd elements of a sequence.

 * is_sequence - Determine if the given object is a sequence (is iterable).

 * conform_list - Ensure that the given object is a list.

 * conform_tuple - Ensure that the given object is a tuple.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: container.py 460 2006-12-10 03:38:13Z james $
"""
__revision__ = "$Revision: 460 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/container.py $"
__all__ = [ 'BidirectionalDictionary', 'merge_dictionaries', 'invert_dictionary', 'dictionary_extract', 'dictionary_subset', 'xzip', 'xenumerate', 'even_elements', 'odd_elements', 'is_sequence', 'conform_list', 'conform_tuple' ]


class BidirectionalDictionary(dict):
    """
    Dictionary that maintains key -> value relationships in both directions.

        >>> input_1 = { 1 : 2 }
        >>> bd = BidirectionalDictionary(input_1)
        >>> bd[1], bd[2]
        (2, 1)
        
        >>> bd.setdefault('foo', 'bar')
        >>> bd['foo'], bd['bar']
        ('bar', 'foo')

        >>> input_2 = { 'a' : 'b' }
        >>> bd.update(input_2)
        >>> bd['a'], bd['b']
        ('b', 'a')

        >>> copy = bd.copy()
        >>> isinstance(copy, BidirectionalDictionary)
        True

        >>> copy == bd
        True

        >>> copy is bd
        False
    """
    def __init__(self, *pos, **kw):
        super(BidirectionalDictionary, self).__init__(*pos, **kw)
        self.resolve()

    def __setitem__(self, key, value):
        super(BidirectionalDictionary, self).__setitem__(key, value)
        super(BidirectionalDictionary, self).__setitem__(value, key)

    def setdefault(self, key, value):
        super(BidirectionalDictionary, self).setdefault(key, value)
        super(BidirectionalDictionary, self).setdefault(value, key)

    def update(self, *pos, **kw):
        super(BidirectionalDictionary, self).update(*pos, **kw)
        self.resolve()
    
    def resolve(self):
        """ Ensure that bidirectional mappings are maintained. """
        value_set = set()
        for key, value in self.items():
            if value in value_set:
                del self[key]
            else:
                value_set.add(key)
        inverse = invert_dictionary(self)
        super(BidirectionalDictionary, self).update(inverse)

    def copy(self):
        return type(self)(self)

    def fromkeys(self, sequence):
        raise AttributeError('%s does not support fromkeys()' % type(self).__name__)


def merge_dictionaries(dictionary, *dictionaries):
    """
    Create a new dictionary with all elements from the given dictionaries.

    Values from dictionaries later (further right) in the argument list replace 
    those with the same keys from earlier dictionaries.

        >>> dict_1 = { 'a' : 1, 'b' : 2 }
        >>> dict_2 = { 'b' : 3, 'c' : 4 }
        >>> dict_3 = { 'c' : 5, 'd' : 6 }
        >>> merged = merge_dictionaries(dict_1, dict_2, dict_3)
        >>> len(merged)
        4

        >>> merged['a'], merged['b'], merged['c'], merged['d']
        (1, 3, 5, 6)
    """
    dictionary = dictionary.copy()
    for dict in dictionaries:
        dictionary.update(dict)
    return dictionary


def invert_dictionary(dictionary):
    """
    Return the 'inverse' of the given dictionary (values become keys).

        >>> my_dict = { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 3 }
        >>> inverse = invert_dictionary(my_dict)
        >>> len(inverse)
        3

        >>> inverse[1], inverse[2], inverse[3]
        ('a', 'b', 'd')
    """
    return dict(reversed(item) for item in dictionary.iteritems())


def dictionary_extract(dictionary, *keys):
    """
    Fetch a subset of the given dictionary, removing the fetched keys from the 
    original dictionary.

        >>> dict_1 = dict(a=1, b=2, c=3, d=4)
        >>> dict_2 = dictionary_extract(dict_1, 'a', 'c')
        
        >>> print sorted(dict_1.keys())
        ['b', 'd']

        >>> print sorted(dict_2.keys())
        ['a', 'c']

        >>> dict_1['b'], dict_1['d']
        (2, 4)

        >>> dict_2['a'], dict_2['c']
        (1, 3)
    """
    return dict((key, dictionary.pop(key)) for key in keys if dictionary.has_key(key))


def dictionary_subset(dictionary, *keys):
    """
    Fetch a subset of the given dictionary, removing the fetched keys from the 
    original dictionary.

        >>> dict_1 = dict(a=1, b=2, c=3, d=4)
        >>> dict_2 = dictionary_subset(dict_1, 'a', 'c')
        
        >>> print sorted(dict_1.keys())
        ['a', 'b', 'c', 'd']

        >>> print sorted(dict_2.keys())
        ['a', 'c']

        >>> dict_1['a'], dict_1['b'], dict_1['c'], dict_1['d']
        (1, 2, 3, 4)

        >>> dict_2['a'], dict_2['c']
        (1, 3)
    """
    return dict((key, dictionary.get(key)) for key in keys if dictionary.has_key(key))


def xzip(*sequences):
    """
    Like zip(), but instead of returning a list, returns an object that 
    generates the zipped sequence on demand.

        >>> seq_1 = [ 1, 2, 3, 4, 5 ]
        >>> seq_2 = [ 'a', 'b', 'c', 'd' ]
        >>> seq_3 = [ 'x', 'y', 'z' ]
        
        >>> for p, q, r in xzip(seq_1, seq_2, seq_3):
        ...     print p, q, r
        1 a x
        2 b y
        3 c z
    """
    if sequences:
        iters = [ iter(s) for s in sequences ]
        while True:
            yield tuple([ i.next() for i in iters ])


def xenumerate(sequence):
    """
    Like enumerate(), but instead of returning a list, returns an object that 
    generates the enumerated sequence in demand.

        >>> sequence = [ 'a', 'b', 'c' ]
        >>> for index, element in xenumerate(sequence):
        ...     print index, element
        0 a
        1 b
        2 c
    """
    counter = 0
    for element in sequence:
        yield counter, element
        counter += 1


def even_elements(sequence):
    """
    Yield only the even elements of a sequence.

    The even_elements function yields the elements of a sequence that have an even index (indices 
    are zero based and zero is considered even).

        >>> sequence = [ 'a', 'b', 'c', 'd', 'e' ]
        >>> list(even_elements(sequence))
        ['a', 'c', 'e']
    """
    i = iter(sequence)
    while True:
        yield i.next()
        i.next()


def odd_elements(sequence):
    """
    Yield only the odd elements of a sequence.

    The odd_elements function yields the elements of a sequence that have an odd index (indices 
    are zero based and zero is considered even).

        >>> sequence = [ 'a', 'b', 'c', 'd', 'e' ]
        >>> list(odd_elements(sequence))
        ['b', 'd']
    """
    i = iter(sequence)
    while True:
        i.next()
        yield i.next()


def is_sequence(obj):
    """
    Determine if the given object is a sequence (is iterable).

    The is_sequence function returns True if the given object is an iterable sequence.

        >>> is_sequence(list())
        True

        >>> is_sequence(dict())
        True

        >>> is_sequence(tuple())
        True

        >>> def generator():
        ...   yield None
        >>> gen = generator()
        >>> is_sequence(gen)
        True
    """
    return hasattr(obj, '__iter__')


def conform_list(obj, strict=False):
    """
    Ensure that the given object is a list.
    If a sequence is passed returns that sequence as a list, otherwise a list 
    containing the single scalar is returned.

    If the strict parameter is true any non-list sequences will be treated as scalars.

        >>> conform_list(list())
        []

        >>> conform_list(tuple())
        []

        >>> conform_list(1)
        [1]

        >>> conform_list((1,2,3))
        [1, 2, 3]

        >>> conform_list((1,2,3), strict=True)
        [(1, 2, 3)]
    """
    if isinstance(obj, list):
        return obj
    if not strict and is_sequence(obj):
        return list(obj)
    return [obj]


def conform_tuple(obj, strict=False):
    """
    Ensure that the given object is a tuple.
    If a sequence is passed returns that sequence as a tuple, otherwise a tuple 
    containing the single scalar is returned.

    If the strict parameter is true any non-tuple sequences will be treated as scalars.

        >>> conform_tuple(tuple())
        ()

        >>> conform_tuple(1)
        (1,)

        >>> conform_tuple([1,2,3])
        (1, 2, 3)

        >>> conform_tuple([1,2,3], strict=True)
        ([1, 2, 3],)
    """
    if isinstance(obj, tuple):
        return obj
    if not strict and is_sequence(obj):
        return tuple(obj)
    return (obj,)


def _test():
    """ Test this module. """
    import doctest
    import container
    return doctest.testmod(container)
