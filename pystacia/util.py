# coding: utf-8
# pystacia/image.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from decorator import decorator


@decorator
def chainable(f, obj, *args, **kw):
    f(obj, *args, **kw)
    
    return obj


# adapted from http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, f):
        self.f = f
        self.cache = {}
        self.__doc__ = f.__doc__
        self.__name__ = f.__name__
        
    def __call__(self, *args, **kw):
        if kw:
            key = args, frozenset(kw.items())
        else:
            key = args
            
        try:
            return self.cache[key]
        except KeyError:
            value = self.f(*args, **kw)
            self.cache[key] = value
            return value


@memoized
def get_osname():
    if hasattr(platform, 'mac_ver') and platform.mac_ver()[0]:
        return 'macos'
    if dist and dist()[0]:
        return 'linux'
    if hasattr(platform, 'win32_ver') and platform.win32_ver()[0]:
        return 'windows'
    # on windows with 2.5 win32_ver is empty
    if version_info[:2] == (2, 5):
        import os
        if os.name == 'nt':
            return 'windows'
        
    return None


class PystaciaException(Exception):
    pass


TinyException = PystaciaException


import platform
from sys import version_info

from pystacia.compat import formattable, dist


from zope.deprecation import deprecated
template = 'Please use tinyimg.util.PystaciaException instead'
deprecated('TinyException', template)