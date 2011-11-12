# coding: utf-8
# pystacia/image.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import with_statement


from decorator import decorator


@decorator
def chainable(f, obj, *args, **kw):
    f(obj, *args, **kw)
    
    return obj


@decorator
def memoized(f, *args, **kw):
    """Decorator that caches a function's return value each time it is called.
    
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated. This decorator performs proper synchronization to make it
    thread-safe.
    """
    if not hasattr(memoized, '__cache'):
        with __lock:
            if not hasattr(memoized, '__cache'):
                memoized.__cache = {}
    
    cache = memoized.__cache 
    key = f, args, frozenset(kw.items())
    if key not in cache:
        with __lock:
            if key not in cache:
                cache[key] = {'lock': Lock()}
                
    key_cache = cache[key]
    if 'value' not in key_cache:
        with key_cache['lock']:
            if 'value' not in key_cache:
                key_cache['value'] = f(*args, **kw)
                
    return key_cache['value']

from threading import Lock

__lock = Lock()


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

from pystacia.compat import dist


from zope.deprecation import deprecated
template = 'Please use tinyimg.util.PystaciaException instead'
deprecated('TinyException', template)
