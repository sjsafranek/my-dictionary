"""
RAZE Python Libraries
Enforced singleton pattern.

 * SingletonError - Exception raised when an attempt is made to create a second 
                    instance of a singleton class.

 * Singleton - Enforce the singleton pattern on derived classes. All classes in
               the heirarchy share a single instance.

 * DerivableSingleton - Enforce the singleton pattern on derived classes. Each class in the 
                        heirarchy stores its own instance.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: singleton.py 372 2006-11-30 03:49:23Z james $
"""
__revision__ = "$Revision: 372 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/singleton.py $"
__all__ = [ 'SingletonError', 'Singleton', 'DerivableSingleton' ]

from threading_ import RLock


class SingletonError(TypeError):
    """ Singleton already instantiated. """
    pass


class MetaSingleton(type):
    """ Perform the actual initialisation of the internal instance. """
    def __call__(class_, *pos, **kw):
        # DCL around instance assignment
        if class_._singleton_instance is None:
            try:
                class_._singleton_mutex.acquire()
                if class_._singleton_instance is None:
                    # first constructor call: create the object
                    class_._singleton_instance = super(MetaSingleton, class_).__call__(*pos, **kw)
                    return class_._singleton_instance
            finally:
                class_._singleton_mutex.release()

        # repeat call: complain if we are attempting to instantiate a derived 
        # class or being passed arguments
        if pos or kw or type(class_._singleton_instance) != class_:
            raise SingletonError('%s singleton already instantiated' % class_)

        return class_._singleton_instance


class MetaDerivableSingleton(MetaSingleton):
    """ Installs instance/mutex attributes into each class. """
    def __new__(metaclass, name, bases, context): 
        context.setdefault('_singleton_instance', None)
        context.setdefault('_singleton_mutex', RLock())
        return MetaSingleton.__new__(metaclass, name, bases, context)


class Singleton(object):
    """
    Singleton base class.
    
    Enforce the singleton pattern on derived classes. All classes in the 
    heirarchy share a single instance.

    A class is deemed a singleton by inheriting from the Singleton base class.
    Multiple constructor calls yield the same singleton instance.

        >>> class Foo(Singleton):
        ...   pass
        >>> x = Foo()
        >>> y = Foo()
        >>> x is y
        True


    Cannot instantiate derived classes if a base has already been instantiated, 
    attempts to do so result in a SingletonError being raised.

        >>> class Bar(Foo):
        ...   pass

        >>> z = Bar()
        Traceback (most recent call last):
        SingletonError: <class 'raze.singleton.Bar'> singleton already instantiated


    Singleton classes that take construction arguments may only recieve the 
    arguments upon the first call. To obtain the singleton instance afterwards 
    simply call the class constructor with no arguments.

        >>> class Spam(Singleton):
        ...   def __init__(self, my_param):
        ...     self.my_param = my_param

        >>> x = Spam(123)
        >>> y = Spam()
        >>> x is y
        True


    Attempts to pass the construction arguments a second time result in a 
    SingletonError being raised.

        >>> z = Spam(321)
        Traceback (most recent call last):
        SingletonError: <class 'raze.singleton.Spam'> singleton already instantiated
    """
    __metaclass__ = MetaSingleton
    _singleton_instance = None
    _singleton_mutex = RLock()


class DerivableSingleton(Singleton):
    """
    Derivable singleton base classes.

    Enforce the singleton pattern on derived classes. Each class in the 
    heirarchy stores its own instance.

        >>> class Foo(DerivableSingleton):
        ...   pass

        >>> class Bar(Foo):
        ...   pass

        >>> x = Foo()
        >>> y = Foo()
        >>> x is y
        True

        >>> z = Bar()
        >>> z is x
        False
    """
    __metaclass__ = MetaDerivableSingleton


def _test():
    """ Test this module. """
    import doctest
    import singleton
    return doctest.testmod(singleton)
