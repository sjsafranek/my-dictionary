"""
RAZE Python Libraries
Networking support classes.

 * IPv4 - IPv4 Address class.

 * CIDR - Represents CIDR 'slash' notation (xxx.xxx.xxx.xxx/yy).


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: net.py 372 2006-11-30 03:49:23Z james $
"""
__revision__ = "$Revision: 372 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/net.py $"
__all__ = [ 'IPv4', 'CIDR' ]

from raze.misc import join


class IPv4(object):
    """
    IPv4 Address.

    IPv4 addresses can be constructed from (and converted to) strings.

        >>> addr = IPv4('192.168.10.23')
        >>> addr.string
        '192.168.10.23'

    octets:

        >>> addr = IPv4(192,168,10,23)
        >>> addr.octets
        (192L, 168L, 10L, 23L)

    or long integers:

        >>> addr = IPv4(3232238103L)
        >>> addr.long
        3232238103L


    IPv4 objects are comparable:

        >>> addr1 = IPv4(192,168,10,23)
        >>> addr2 = IPv4(192,168,10,240)

        >>> addr1 == addr2
        False

        >>> addr1 < addr2
        True
    """
    def __init__(self, *pos):
        self._long = 0L
        if len(pos) == 4:
            self.octets = pos
        elif len(pos) == 1:
            arg = pos[0]
            if isinstance(arg, basestring):
                self.string = arg
            else:
                self.long = arg
        else:
            raise TypeError('Could not initialise IPv4 object from "%s".' % join(pos))

    def get_octets(self):
        """ 4-tuple containing each octet of this address. """
        a = (self.long >> 24L) & 255L 
        b = (self.long >> 16L) & 255L
        c = (self.long >>  8L) & 255L
        d = (self.long >>  0L) & 255L
        return a, b, c, d
    def set_octets(self, value):
        if len(value) != 4:
            raise TypeError('Invalid octets sequence: %s.' % value)
        self.long  = (long(value[0]) << 24L)
        self.long |= (long(value[1]) << 16L)
        self.long |= (long(value[2]) << 8L)
        self.long |= (long(value[3]) << 0L)
    octets = property(get_octets, set_octets)

    def get_string(self):
        """ Dotted-quad string representation of this IP address. """
        return '%d.%d.%d.%d' % tuple(self.octets)
    def set_string(self, value):
        import socket
        try:
            value = socket.inet_aton(value)
        except socket.error:
            raise TypeError('Invalid IPv4 address string: "%s".' % value)
        self.octets = [ ord(c) for c in value ]
    string = property(get_string, set_string)
    
    def get_long(self):
        """ Long integer representation of this IP address. """
        return self._long
    def set_long(self, value):
        self._long = long(value)
    long = property(get_long, set_long)

    def make_cidr(self, cidr):
        """ Construct a CIDR object using the given bit count. """
        return CIDR(self, cidr)

    def __div__(self, cidr):
        """ Construct a CIDR object using the given bit count. """
        return self.make_cidr(cidr)

    def __cmp__(self, other):
        class_ = type(self)
        if not isinstance(other, class_):
            other = class_(other)
        return cmp(self.long, other.long)

    def __str__(self):
        return self.string

    def __long__(self):
        return self.long

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)


class CIDR(object):
    """
    Represents CIDR 'slash' notation (xxx.xxx.xxx.xxx/yy).

    A CIDR object can be obtained from an IPv4 object by specifying the CIDR value using the divide operator:

        >>> addr1 = IPv4(192,168,10,23)
        >>> addr2 = IPv4(192,168,10,240)

        >>> cidr = addr1 / 24
        >>> cidr.address_count
        256L

        >>> cidr.network
        IPv4(192.168.10.0)

        >>> cidr.broadcast
        IPv4(192.168.10.255)

        >>> addr2 in cidr
        True
    """
    def __init__(self, address, cidr):
        if not isinstance(address, IPv4):
            address = IPv4(address)
        self.address = address
        self.cidr = long(cidr)

    @property
    def network(self):
        return IPv4(self.address.long & self.subnet_mask.long)

    @property
    def broadcast(self):
        return IPv4(self.network.long + self.address_count - 1)

    @property
    def subnet_mask(self):
        long = 0L
        for i in range(self.cidr):
            long |= 1L << (31L - i)
        return IPv4(long)

    @property
    def address_count(self):
        return 2 ** (32 - self.cidr)

    @property
    def addresses(self):
        return list(self)

    def __contains__(self, address):
        if not isinstance(address, IPv4):
            address = IPv4(address)
        return address >= self.network and address <= self.broadcast

    def __len__(self):
        return self.address_count
    
    def __iter__(self):
        for long in range(self.network.long, self.broadcast.long):
            yield IPv4(long)

    def __str__(self):
        return '%s/%d' % (self.address, self.cidr)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)


def _test():
    """ Test this module. """
    import doctest
    import net
    return doctest.testmod(net)
