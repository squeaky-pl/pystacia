# coding: utf-8
# pystacia/registry.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import with_statement

from threading import Lock


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

from pystacia.compat import formattable
from pystacia.util import PystaciaException
