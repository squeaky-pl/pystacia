# coding: utf-8
# pystacia/lazyenum.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


class Enum(object):
    def __init__(self, name):
        self.name = name
        
    def __getattr__(self, name):
        return enum_value(self, name)
    
    def __repr__(self):
        template = formattable("pystacia.lazyenum.enum('{0}')")
        
        return template.format(self.name)


class EnumValue(object):
    def __init__(self, enum, name):
        self.enum = enum
        self.name = name
        
    def __repr__(self):
        return repr(self.enum) + '.' + self.name

from pystacia.util import memoized


@memoized
def enum(name):
    return Enum(name)


@memoized
def enum_value(enum, name):
    return EnumValue(enum, name)


from pystacia.compat import formattable
