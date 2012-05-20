# coding: utf-8

# pystacia/util.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import with_statement

from sys import version_info
import platform
from threading import Lock, RLock

from decorator import decorator


class Registry(object):
    def __init__(self, defaults=None):
        self.__dict__.update({
            '_Registry__lock': Lock(),
            '_Registry__locked': [],
            '_Registry__defaults': defaults or {}})

    def _install_default(self, key, value):
        with self.__lock:
            self.__defaults[key] = value

    def _lock(self, key):
        with self.__lock:
            if key in self.__locked:
                msg = formattable("Key '{0}' has been already locked")
                raise PystaciaException(msg.format(key))

            self.__locked.append(key)

    def get(self, key, value=None, override=None, lock=False):
        if lock:
            self._lock(key)

        if override != None:
            return override

        if key in self.__dict__:
            with self.__lock:
                if key in self.__dict__:
                    return self.__dict__[key]

        if key in self.__defaults:
            with self.__lock:
                if key in self.__defaults:
                    return self.__defaults[key]

        return value

    def __getattr__(self, key):
        if key in self.__defaults:
            with self.__lock:
                if key in self.__defaults:
                    return self.__defaults[key]

        msg = '{0} object has no attribute {1}, neither found in defaults'
        raise AttributeError(formattable(msg).format(self.__class__, key))

    def __setattr__(self, key, value):
        with self.__lock:
            if key in self.__locked:
                msg = formattable("Key '{0}' has been locked")
                raise PystaciaException(msg.format(key))

            self.__dict__[key] = value

    def __delattr__(self, key):
        with self.__lock:
            if key in self.__locked:
                msg = formattable("Key '{0}' has been locked")
                raise PystaciaException(msg.format(key))

            del self.__dict__[key]


@decorator
def chainable(f, obj, *args, **kw):
    f(obj, *args, **kw)

    return obj


# memoized cache
__cache = {}


@decorator
def memoized(f, *args, **kw):
    """Decorator that caches a function's return value each time it is called.

    If called later with the same arguments, the cached value is returned, and
    not re-evaluated. This decorator performs proper synchronization to make it
    thread-safe.
    """
    key = f, args, frozenset(kw.items())
    if key not in __cache:
        with __lock:
            if key not in __cache:
                __cache[key] = {'lock': RLock()}

    key_cache = __cache[key]
    if 'value' not in key_cache:
        with key_cache['lock']:
            if 'value' not in key_cache:
                info = key[0].__name__, key[1]
                msg = formattable('Memoizing {0} args={1}').format(*info)
                logger.debug(msg)

                result = f(*args, **kw)

                key_cache['value'] = result
                msg = formattable('Memoized {0} args={1}').format(*info)
                logger.debug(msg)

    return key_cache['value']

__lock = Lock()


@memoized
def get_osname():
    if hasattr(platform, 'win32_ver') and platform.win32_ver()[0]:
        return 'windows'
    # on windows with 2.5 win32_ver is empty
    if version_info[:2] == (2, 5):
        import os
        if os.name == 'nt':
            return 'windows'
    if hasattr(platform, 'mac_ver') and platform.mac_ver()[0]:
        return 'macos'
    if dist and dist()[0]:
        # beware that under ssh/MSYS and Windows it returns Debian!
        return 'linux'

    return None


class PystaciaException(Exception):
    pass


TinyException = PystaciaException

from pystacia.compat import dist, formattable
from pystacia import logger


from zope.deprecation import deprecated  # @UnresolvedImport
template = 'Please use tinyimg.util.PystaciaException instead'
deprecated('TinyException', template)
