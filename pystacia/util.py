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


@decorator
def only_live(f, obj, *args, **kw):
    if obj.closed:
        template = formattable('{0} already closed')
        raise TinyException(template.format(obj.__class__))
    
    return f(obj, *args, **kw)


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
        
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.f(*args)
            self.cache[args] = value
            return value


def find_library(name, abis):
    paths = []
    
    try:
        path = environ['PYSTACIA_LIBRARY_PATH']
    except KeyError:
        pass
    else:
        paths.append(path)
    
    osname = get_osname()
    
    if not environ.get('PYSTACIA_SKIP_PACKAGE'):
        import pystacia
        path = dirname(pystacia.__file__)
        paths.append(join(path, 'cdll'))
    
    if not environ.get('PYSTACIA_SKIP_VIRTUAL_ENV'):
        try:
            path = environ['VIRTUAL_ENV']
        except KeyError:
            pass
        else:
            paths.append(join(path, 'lib'))
            paths.append(join(path, 'dll'))
    
    from os import getcwd
    paths.append(getcwd())
    
    from ctypes import CDLL
    dll_template = None
    factory = CDLL

    def dll_template(abi):
        if osname == 'macos':
            return 'lib{name}.{abi}.dylib' if abi else 'lib{name}.dylib'
        elif osname == 'linux':
            return 'lib{name}.so.{abi}' if abi else 'lib{name}.so'
        elif osname == 'windows':
            return 'lib{name}-{abi}.dll' if abi else 'lib{name}.dll'
        
        return None

    for path in paths:
        if not exists(path):
            continue
        
        depends_path = join(path, 'depends.txt')
        if exists(depends_path):
            depends = open(depends_path)
            
            for line in depends:
                depname, depabi = line.split()
                template = formattable(dll_template(depabi))
                dll_path = join(path, template.format(name=depname,
                                                      abi=depabi))
                try:
                    factory(dll_path)
                except:
                    pass
            
            depends.close()
        
        for abi in abis:
            template = formattable(dll_template(abi))
            if not template:
                continue
            dll_path = join(path, template.format(name=name, abi=abi))
            if exists(dll_path):
                transaction = library_path_transaction(path).begin()
                
                try:
                    factory(dll_path)
                except:
                    transaction.rollback()
                else:
                    transaction.commit()
                    return dll_path
    
    return None


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


class library_path_transaction:
    _environ_keys = dict(macos='DYLD_FALLBACK_LIBRARY_PATH',
                         linux='LD_LIBRARY_PATH',
                         windows='PATH')
    
    def __init__(self, path):
        self.key = self.__class__._environ_keys[get_osname()]
        self.path = path
        
    def begin(self):
        old_path = environ.get(self.key)
        if not old_path or self.path not in old_path:
            parts = [self.path]
            if old_path:
                parts.append(old_path)
            environ[self.key] = pathsep.join(parts)
        
        self.old_path = old_path
        environ['MAGICK_HOME'] = self.path
        
        return self
        
    def commit(self):
        return self
    
    def rollback(self):
        if self.old_path:
            environ[self.key] = self.old_path
        else:
            del environ[self.key]
            
        del environ['MAGICK_HOME']
        
        return self


class TinyException(Exception):
    pass


import platform
from sys import version_info
from os import environ, pathsep
from os.path import join, exists, dirname

from pystacia.compat import formattable, dist
