# coding: utf-8
# pystacia/lazyenum.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from six import string_types


class Enum(object):
    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        return self.cast(name)

    def cast(self, name):
        return cast(self, name)

    def __str__(self):
        return self.name

    def __repr__(self):
        template = formattable("pystacia.lazyenum.enum('{0}')")

        return template.format(self.name)


class EnumValue(object):
    def __init__(self, enum, name):
        self.enum = enum
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.enum) + '.' + self.name

    def __eq__(self, other):
        try:
            other = self.enum.cast(other)
        except CastException:
            return False

        return self is other

    def __hash__(self):
        return hash((self.enum.name, self.name))

from pystacia.util import memoized


@memoized
def enum(name):
    return Enum(name)


@memoized
def enum_value(enum, name):
    return EnumValue(enum, name)


def cast(enum_, name):
    if isinstance(enum_, Enum):
        pass
    elif isinstance(enum_, string_types):
        enum_ = enum(enum_)
    else:
        msg = formattable('Cannot cast {0} to Enum')
        raise CastException(msg.format(enum_))

    if isinstance(name, EnumValue):
        if name.enum != enum_:
            msg = formattable('Attempted to cast {0} to unrelated Enum {1}')
            raise CastException(msg.format(str(name), str(enum_)))

        return name
    elif isinstance(name, string_types):
        return enum_value(enum_, name)
    else:
        msg = formattable('Cannot cast {0} to EnumValue with Enum {1}')
        raise CastException(msg.format(str(name), str(enum_)))

from pystacia.util import PystaciaException


class CastException(PystaciaException):
    pass


from pystacia.compat import formattable
