"""
Extensions and helpers to the standard os.path module.

 * expand_path - Resolve a path to it's full expanded name.

 * recursive_mkdir - Recursively make directories (similar to os.path.makedirs, 
                     but does not raise an exception if any of the directories 
                     in the path already exist).


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: path.py 428 2006-12-04 10:22:03Z system $
"""
__revision__ = "$Revision: 428 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/path.py $"
__all__ = [ 'expand_path', 'recursive_mkdir' ]

import os.path


def expand_path(path):
    """ Resolve a path to it's full expanded name. """
    path = os.path.expanduser(path)
    path = os.path.realpath(path)
    return os.path.normpath(path)


def recursive_mkdir(path):
    """
    Recursively make directories (similar to os.path.makedirs, but does not 
    raise an exception if any of the directories in the path already exist).
    """
    path    = expand_path(path)
    chunks  = path.split(os.path.sep)
    current = os.path.sep
    for chunk in chunks[1:]:
        current = os.path.join(current, chunk)
        if not os.path.exists(current):
            os.mkdir(current)


def _test():
    """ Test this module. """
    import doctest
    import path
    return doctest.testmod(path)
