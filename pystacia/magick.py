# coding: utf-8
# pystacia/image.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.util import memoized


@memoized
def get_version():
    options = get_options()
    
    try:
        version = options['LIB_VERSION_NUMBER']
    except KeyError:
        try:
            version = options['VERSION']
        except KeyError:
            return None
        else:
            return tuple(int(x) for x in version.split('.'))
    else:
        return tuple(int(x) for x in version.split(','))


@memoized
def get_options():
    def get_options_real():
        options = {}
        
        from ctypes import c_size_t
        from six import b
        from pystacia.compat import native_str
        
        size = c_size_t()
        keys = cdll.MagickQueryConfigureOptions(b('*'), size)
        for key in (keys[i] for i in range(size.value)):
            options[native_str(key)] =\
            native_str(cdll.MagickQueryConfigureOption(key))
            
        return options
    
    def get_options_hack(path):
        options = {}
        
        parser = ElementTree()
        root = parser.parse(path)
        for element in root.findall('configure'):
            attrs = element.attrib
            options[attrs['name']] = attrs['value']
            
        return options
    
    dll_path = dirname(cdll._name)
    config_path = join(dll_path, 'configure.xml')
    
    if exists(config_path):
        return get_options_hack(config_path)
    else:
        return get_options_real()


def get_version_str():
    return cdll.MagickGetVersion(None)


def get_delegates():
    try:
        delegates = get_options()['DELEGATES']
    except KeyError:
        return []
    
    return delegates.split()


def get_depth():
    depth = get_options().get('QuantumDepth')
    return int(depth) if depth else None

from os.path import dirname, join, exists

try:
    from xml.etree.cElementTree import ElementTree
except ImportError:
    from xml.etree.ElementTree import ElementTree  # @Reimport

from pystacia import cdll
