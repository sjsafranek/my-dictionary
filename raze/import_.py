"""
RAZE Python Libraries
Import related utilities.

 * LazyImport - Lazy module importer, acts as a proxy for a given module, 
                importing it upon first use.

 * import_ - Import an object given a fully qualified name.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: import_.py 366 2006-11-30 00:48:04Z james $
"""
__revision__ = "$Revision: 366 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/import_.py $"
__all__ = [ 'LazyImport', 'import_' ]


class LazyImport(object):
    """
    Lazy module importer, acts as a proxy for a given module, importing it upon first use.

    This class is useful when a module cannot be imported into the global namespace 
    due to cyclic dependencies.

        >>> mod = LazyImport('raze.misc')
        >>> mod.SimpleObject
        <class 'raze.misc.SimpleObject'>
    """
    __slots__ = '__module_name'

    def __init__(self, module_name):
        super(LazyImport, self).__init__()
        self.__module_name = module_name

    @property
    def __module(self):
        return import_(self.__module_name)

    def __getattr__(self, name):
        return getattr(self.__module, name)
    
    def __setattr__(self, name, value):
        if name.startswith('_LazyImport__'):
            super(LazyImport, self).__setattr__(name, value)
        else:
            setattr(self.__module, name, value)
    
    def __delattr__(self, name):
        delattr(self.__module, name)


def import_(qualified_name):
    """
    Import an object given a fully qualified name.

        >>> from raze.misc import SimpleObject
        >>> so = import_('raze.misc.SimpleObject')
        >>> so is SimpleObject
        True
    """
    module_name, name = qualified_name.rsplit('.', 1)
    module = __import__(module_name, {}, {}, [name])
    return getattr(module, name)


def _test():
    """ Test this module. """
    import doctest
    import import_
    return doctest.testmod(import_)
