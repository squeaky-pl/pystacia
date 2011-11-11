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
    if environ.get('PYSTACIA_SKIP_MEMOIZE'):
        return f(*args, **kw)

    if not hasattr(memoized, '__cache'):
        with __lock:
            if not hasattr(memoized, '__cache'):
                memoized.__cache = {}
                
    if f not in memoized.__cache:
        with __lock:
            if not f in memoized.__cache:
                memoized.__cache[f] = {}
    
    f_cache = memoized.__cache[f] 
    key = args, frozenset(kw.items())
    if key not in f_cache:
        with __lock:
            if key not in f_cache:
                f_cache[key] = {'lock': RLock()}
                
    key_cache = f_cache[key]
    if 'value' not in key_cache:
        with key_cache['lock']:
            if 'value' not in key_cache:
                result = f(*args, **kw)
                if 'value' not in key_cache:
                    key_cache['value'] = result
                
    return key_cache['value']

from threading import RLock, Lock

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
from os import environ

from pystacia.compat import formattable, dist


from zope.deprecation import deprecated
template = 'Please use tinyimg.util.PystaciaException instead'
deprecated('TinyException', template)