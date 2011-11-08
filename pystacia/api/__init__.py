# coding: utf-8
# pystacia/api/__init__.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import with_statement


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
    
    dll_template = None

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
                    CDLL(dll_path)
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
                    CDLL(dll_path)
                except:
                    transaction.rollback()
                else:
                    transaction.commit()
                    return dll_path
    
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


from threading import Lock

__lock = Lock()

def get_dll(init=True):
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
                # first let's look in some places that may override system-wide paths
                path = find_library(name, abis)
                # still nothing? let ctypes figure it out
                if not path:
                    path = ctypes.util.find_library(name)
                if not path:
                    raise PystaciaException('Could not find or load MagickWand')
                
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
            # should be delayed on initialization
            # warn if unsupported
            # from pystacia import magick
            # from pystacia.api import min_version
            #version = magick.get_version()
            #if version < min_version:
            #    from warnings import warn
            #    template = formattable('Unsupported version of MagickWand {0}')
            #    warn(template.format(version))
    
    return dll


from os import environ, pathsep
from os.path import join, exists, dirname
from ctypes import CDLL
import ctypes.util
import atexit

from pystacia import logger
from pystacia.util import get_osname, PystaciaException
from pystacia.compat import formattable
from pystacia.common import _cleanup
from pystacia.api.func import get_bridge, simple_call, call



min_version = (6, 5, 9, 0)
name = 'MagickWand'
abis = (5, 4, 3, None)
