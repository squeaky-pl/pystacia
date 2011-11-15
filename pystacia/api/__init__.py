# coding: utf-8
# pystacia/api/__init__.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import with_statement

from logging import getLogger

logger = getLogger('pystacia.api')


def dll_template(osname, abi):
    if osname == 'macos':
        return 'lib{name}.{abi}.dylib' if abi else 'lib{name}.dylib'
    elif osname == 'linux':
        return 'lib{name}.so.{abi}' if abi else 'lib{name}.so'
    elif osname == 'windows':
        return 'lib{name}-{abi}.dll' if abi else 'lib{name}.dll'
    
    return None


def find_library(name, abis, environ=None, osname=None, factory=None):
    paths = []
    
    if not environ:
        environ = os.environ
    
    try:
        path = environ['PYSTACIA_LIBRARY_PATH']
    except KeyError:
        pass
    else:
        paths.append(path)
    
    if not osname:
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
    
    if not environ.get('PYSTACIA_SKIP_CWD'):
        from os import getcwd
        paths.append(getcwd())
    
    if not factory:
        factory = CDLL
    
    for path in paths:
        if not exists(path):
            continue
        
        depends_path = join(path, 'depends.txt')
        if exists(depends_path):
            depends = open(depends_path)
            
            for line in depends:
                depname, depabi = line.split()
                template = formattable(dll_template(osname, depabi))
                dll_path = join(path, template.format(name=depname,
                                                      abi=depabi))
                try:
                    factory(dll_path)
                except:
                    pass
            
            depends.close()
        
        for abi in abis:
            template = dll_template(osname, abi)
            if not template:
                continue
            
            template = formattable(template)
            
            dll_path = join(path, template.format(name=name, abi=abi))
            if exists(dll_path):
                transaction = library_path_transaction(path, environ).begin()
                
                try:
                    factory(dll_path)
                except:
                    from sys import exc_info
                    msg = formattable('Caught exception while loading '
                                      '{0}: {1}. Rolling back')
                    logger.debug(msg.format(dll_path, exc_info()[1]))
                    transaction.rollback()
                else:
                    transaction.commit()
                    return dll_path
    
    # still nothing? let ctypes figure it out
    if not environ.get('PYSTACIA_SKIP_SYSTEM'):
        return ctypes.util.find_library(name)

    return None


class library_path_transaction:
    _environ_keys = dict(macos='DYLD_FALLBACK_LIBRARY_PATH',
                         linux='LD_LIBRARY_PATH',
                         windows='PATH')
    
    def __init__(self, path, environ=None):
        self.environ = environ or os.environ
        self.key = self.__class__._environ_keys[get_osname()]
        self.path = path
        
    def begin(self):
        environ = self.environ
        self.old_path = old_path = environ.get(self.key)
        if not old_path or self.path not in old_path:
            parts = [self.path]
            if old_path:
                parts.append(old_path)
            environ[self.key] = pathsep.join(parts)
        
        environ['MAGICK_HOME'] = self.path
        
        return self
        
    def commit(self):
        return self
    
    def rollback(self):
        environ = self.environ
        if self.old_path:
            environ[self.key] = self.old_path
        else:
            del environ[self.key]
            
        del environ['MAGICK_HOME']
        
        return self

from threading import Lock

__lock = Lock()


def get_dll(init=True, environ=None):
    """Find ImageMagick DLL and initialize it.
       
       Searches available paths with :func:`find_library`
       and then fallbacks to standard :func:`ctypes.util.find_liblrary`.
       Loads the DLL into memory, initializes it and warns if it has
       unsupported API and ABI versions.
    """
    if not hasattr(get_dll, '__dll'):
        logger.debug('Critical section - load MagickWand')
        with __lock:
            if not hasattr(get_dll, '__dll'):
                if not environ:
                    environ = os.environ
                
                path = find_library(name, abis, environ=environ)
                if not path:
                    msg = 'Could not find or load MagickWand'
                    raise PystaciaException(msg)
                
                msg = formattable('Loading MagickWand from {0}')
                logger.debug(msg.format(path))
                get_dll.__dll = CDLL(path)
                get_dll.__dll.__inited = False
        
    dll = get_dll.__dll

    if init and not dll.__inited:
        def shutdown():
            logger.debug('Cleaning up traced instances')
            _cleanup()
            
            simple_call(None, 'terminus')
            
            logger.debug('Shutting down the bridge')
            get_bridge().shutdown()
        
        logger.debug('Critical section - init MagickWand')
        with __lock:
            if not dll.__inited:
                simple_call(None, 'genesis', __init=False)
                
                logger.debug('Registering atexit handler')
                atexit.register(shutdown)
                
                dll.__inited = True
                
        version = magick.get_version()
        if version < min_version:
            msg = formattable('Unsupported version of MagickWand {0}')
            warn(msg.format(version))
    
    return dll

from pystacia.util import memoized


@memoized
def get_bridge(environ=None):
    if not environ:
        environ = os.environ
        
    if environ.get('PYSTACIA_IMPL', '').upper() == 'SIMPLE':
        logger.debug('Using Simple implementation')
        impl = SimpleImpl()
    else:
        logger.debug('Using Thread implementation')
        impl = ThreadImpl(True)
        
    bridge = CallBridge(impl)
    
    return bridge


import os
from os import pathsep
from os.path import join, exists, dirname
from ctypes import CDLL
import ctypes.util
from warnings import warn
import atexit

from pystacia.bridge import CallBridge, ThreadImpl, SimpleImpl
from pystacia.util import get_osname, PystaciaException
from pystacia.compat import formattable
from pystacia.common import _cleanup
from pystacia import magick
from pystacia.api.func import simple_call


min_version = (6, 5, 9, 0)
name = 'MagickWand'
abis = (5, 4, 3, None)
