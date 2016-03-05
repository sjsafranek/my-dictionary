"""
RAZE Python Libraries
Password generation and other utilities.

 * generate_password - Generate a password that conforms to the given parameters.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: password.py 372 2006-11-30 03:49:23Z james $
"""
__revision__ = "$Revision: 372 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/password.py $"
__all__ = [ 'generate_password' ]

from random import choice, randint
from phonetic import CharacterSets
from container import merge_dictionaries
from misc import Default, join


def generate_password(min_length=8, max_length=Default, **character_sets):
    """
    Generate a password.

    Additional keyword parameteters specify which character sets to use (from 
    phonetic.CharacterSets).  The default character sets are 'lower_case', 
    'upper_case' and 'digits'.

        >>> pwd = generate_password()
        >>> len(pwd)
        8

        >>> pwd = generate_password(lower_case=True)
        >>> lower_case = set(CharacterSets.lower_case.keys())
        >>> lower_case.issuperset(pwd)
        True
    """
    if not character_sets:
        character_sets['lower_case'] = True
        character_sets['upper_case'] = True
        character_sets['digits'] = True

    character_sets = [ getattr(CharacterSets, name) for name, allow in character_sets.iteritems() if allow ]
    character_set  = merge_dictionaries(*character_sets).keys()

    if max_length is Default:
        max_length = min_length
    
    length = randint(min_length, max_length)
    result = [ choice(character_set) for index in xrange(length) ]
    return join(result, separator='')


def _test():
    """ Test this module. """
    import doctest
    import password
    return doctest.testmod(password)
