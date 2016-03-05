"""
RAZE Python Libraries
Classes for simple implementation of the visitor pattern.

 * Visitor - Base class for visitor objects.

 * Visitee - Base class for objects that may be visited.

 * VisiteeAdapter - Adapt any object to the Visitee interface.

 * visit - Helper function that adapts the given visitee to the Visitee 
           interface before calling visitee.accept_visitor(visitor).


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: visitor.py 364 2006-11-30 00:12:28Z james $
"""
__revision__ = "$Revision: 364 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/visitor.py $"
__all__ = [ 'VisitError', 'Visitor', 'Visitee', 'visit' ]

from inspect import getmro
from protocols import adapt, advise, AbstractBase
from namestyle import NameStyleConverter


class VisitError(TypeError):
    """ Raised when a visitor does not support the type of the visitee. """
    pass


class Visitor(object):
    """
    Base class for visitor objects.

    The visitor object is written with methods matching the .visitor_method for each 
    type it needs to handle. Following is a visitor that handles visitation of Foo 
    and Bar objects.

        >>> class MyVisitor(Visitor):
        ...   def visit_foo(self, obj):
        ...     print 'Visited a Foo!'
        ...   def visit_bar(self, obj):
        ...     print 'Visited a Bar!'
        ...   def visit_int(self, obj):
        ...     print 'Visited an integer (%d)!' % obj
        >>> visitor = MyVisitor()

        >>> class Foo(Visitee): pass
        >>> class Bar(Visitee): pass
        >>> class Baz(Visitee): pass
        >>> foo = Foo()
        >>> bar = Bar()
        >>> baz = Baz()

        >>> foo.accept_visitor(visitor)
        Visited a Foo!

        >>> bar.accept_visitor(visitor)
        Visited a Bar!

    Attempting to visit an unsupported visitor type raises a VisitError.   

        >>> try:
        ...   baz.accept_visitor(visitor)
        ... except VisitError, e:
        ...   expected = 'MyVisitor does not support visitation of Baz (%r).' % baz
        ...   assert(str(e) == expected)

    By default a visitee traverses it's MRO (method resolution order) looking for a method to call.
    This provides support for inheritance.

        >>> class Spam(Foo): pass
        >>> spam = Spam()
        >>> spam.accept_visitor(visitor)
        Visited a Foo!
    """
    def visit_visitee(self, visitee):
        """ Default visitee handler - raises a VisitError """
        raise VisitError('%s does not support visitation of %s (%r).' % (type(self).__name__, type(visitee).__name__, visitee))


class Visitee(AbstractBase):
    """
    Base class for objects that may be visited.
    
    The 'visitor_method' property of a visitee determines which method to call. By 
    default it uses raze.NameStyleConverter to convert the visitee's class name to 
    'lower' style, and prefixes it with 'visit_'.

        >>> class VisiteeWithLongName(Visitee): pass
        >>> visitee = VisiteeWithLongName()
        >>> visitee.visitor_method(VisiteeWithLongName)
        'visit_visitee_with_long_name'
    """
    visitor_method_format = 'visit_%s'

    def visitor_method(self, class_):
        """
        Return the name of the method to attempt to call when visting objects of 
        this type.
        """
        converter = NameStyleConverter(class_.__name__)
        return self.visitor_method_format % converter.lower

    def visitor_mro(self):
        """
        Return a list of methods to attempt to call on the visitor passed to 
        self.accept_visitor().
        """
        return [ self.visitor_method(class_) for class_ in getmro(type(self.visitee_object)) ]

    @property
    def visitee_object(self):
        """ The actual object to be visited. """
        return self

    def accept_visitor(self, visitor):
        """
        Look for a method of visitor with the name returned by 
        self.visitor_method and call it with self as the only parameter. If 
        visitor does not have such an attribute call visitor.visit(self) 
        instead.
        """
        visitor = adapt(visitor, Visitor)
        for name in self.visitor_mro():
            if hasattr(visitor, name):
                return getattr(visitor, name)(self.visitee_object)
        return visitor.visit_visitee(self)


class VisiteeAdaptor(Visitee):
    """ Adapt any object to the Visitee interface. """
    advise(instancesProvide  = [ Visitee ],
           asAdapterForTypes = [ object ])
    
    def __init__(self, obj):
        super(VisiteeAdaptor, self).__init__()
        self.__object = obj

    @property
    def visitee_object(self):
        """ The actual object to be visited. """
        return self.__object

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.visitee_object)


def visit(visitee, visitor):
    """
    Helper function that adapts the given visitee to the Visitee interface 
    before calling visitee.accept_visitor(visitor).

        >>> class MyVisitor(Visitor):
        ...   def visit_foo(self, obj):
        ...     print 'Visited a Foo!'
        ...   def visit_bar(self, obj):
        ...     print 'Visited a Bar!'
        ...   def visit_int(self, obj):
        ...     print 'Visited an integer (%d)!' % obj
        >>> visitor = MyVisitor()

        >>> class Foo(Visitee): pass
        >>> class Bar(Visitee): pass
        >>> class Baz(Visitee): pass
        >>> foo = Foo()
        >>> bar = Bar()
        >>> baz = Baz()

        >>> visit(foo, visitor)
        Visited a Foo!

    Any object may be used as a visitor by using the visit adaptor.

        >>> visit(1, visitor)
        Visited an integer (1)!
    """
    visitee = adapt(visitee, Visitee)
    return visitee.accept_visitor(visitor)


def _test():
    """ Test this module. """
    import doctest
    import visitor
    return doctest.testmod(visitor)
