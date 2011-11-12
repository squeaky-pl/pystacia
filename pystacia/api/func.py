# coding: utf-8
# pystacia/api/func.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.util import memoized

@memoized
def get_data():
    # convenience shortcuts
    w = MagickWand_p
    pw = PixelWand_p
    b = MagickBoolean
    e = enum
    ch = c_char_p
    v = c_void_p
    P = POINTER
    s = c_size_t
    ss = c_ssize_t
    d = c_double
    u = c_uint
    
    def magick_format(name):
        return 'Magick' + ''.join(x.title() for x in name.split('_'))
    
    
    def image_format(name):
        if isinstance(name, string_types):
            verb = name
            noun = ''
        elif hasattr(name, '__getitem__') and len(name) == 2:
            verb = name[0]
            noun = name[1]
        else:
            raise PystaciaException('Incorrect name format')
        
        return ('Magick' + ''.join(x.title() for x in verb.split('_')) + 'Image' +
                ''.join(x.title() for x in noun.split('_')))
    
    
    def pixel_format(name):
        if name == 'get_hsl':
            name = 'GetHSL'
        else:
            name = ''.join(x.title() for x in name.split('_'))
        return 'Pixel' + name
    
    return {
        None: {
            'format': lambda name: 'MagickWand' + name.title(),
            'symbols': {
                'genesis': ((),),
                'terminus': ((),),
            }
        },
        
        'magick': {
            'format': magick_format,
            'arg': MagickWand_p,
            'symbols': {
                'set_size': ((c_size_t, c_size_t), MagickBoolean),
                'get_format': ((), c_char_p),
                'set_format': ((c_char_p,), MagickBoolean),
                'set_depth': ((c_size_t,), MagickBoolean),
                'get_exception': ((POINTER(ExceptionType),), c_void_p)
            }
        },
            
        'magick_': {
            'format': magick_format,
            'symbols': {
                'query_configure_options': ((c_char_p, POINTER(c_size_t)),
                                            POINTER(c_char_p)),
                'query_configure_option': ((c_char_p,), c_char_p),
                'get_version': ((POINTER(c_size_t),), c_char_p),
                'relinquish_memory': ((c_void_p,), c_void_p)
            }
        },
        
        'wand': {
            'format': lambda name: name.title() + 'MagickWand',
            'result': MagickWand_p,
            'symbols': {
                'new': ((),),
                'clone': ((MagickWand_p,),),
                'destroy': ((MagickWand_p,),)
            }
        },
            
        'pwand': {
            'format': lambda name: name.title() + 'PixelWand',
            'result': PixelWand_p,
            'symbols': {
                'new': ((),),
                'clone': ((PixelWand_p,),),
                'destroy': ((PixelWand_p,),)
            }
        },
            
        'image': {
            'format': image_format,
            'arg': MagickWand_p,
            'symbols': {
                'read': ((c_char_p,), MagickBoolean),
                'write': ((c_char_p,), MagickBoolean),
                ('read', 'blob'): ((c_void_p, c_size_t), MagickBoolean),
                ('get', 'blob'): ((POINTER(c_size_t),), c_void_p),
                
                ('set', 'format'): ((c_char_p,), MagickBoolean),
                ('get', 'format'): ((), c_char_p),
                ('set', 'compression_quality'): ((c_size_t,), MagickBoolean),
                ('get', 'compression_quality'): ((), c_size_t),
                ('get', 'width'): ((), c_size_t),
                ('get', 'height'): ((), c_size_t),
                ('get', 'depth'): ((), c_size_t),
                ('set', 'depth'): ((c_size_t,), MagickBoolean),
                ('get', 'type'): ((), enum),
                ('set', 'type'): ((enum,), MagickBoolean),
                ('get', 'colorspace'): ((), enum),
                ('set', 'colorspace') : ((enum,), MagickBoolean),
                ('get', 'pixel_color'): ((c_ssize_t, c_ssize_t, PixelWand_p),
                                         MagickBoolean),
                ('set', 'background_color'): ((PixelWand_p,), MagickBoolean),
                ('get', 'background_color'): ((PixelWand_p,), MagickBoolean),
                ('transform', 'colorspace'): ((enum,), MagickBoolean),
                
                'resize': ((c_size_t, c_size_t, enum, c_double), MagickBoolean),
                'crop': ((c_size_t, c_size_t, c_ssize_t, c_ssize_t), MagickBoolean),
                'rotate': ((PixelWand_p, c_double), MagickBoolean),
                'flip': ((), MagickBoolean),
                'flop': ((), MagickBoolean),
                'transpose': ((), MagickBoolean),
                'transverse': ((), MagickBoolean),
                'shear': ((PixelWand_p, c_double, c_double), MagickBoolean),
                'roll': ((c_ssize_t, c_ssize_t), MagickBoolean),
                'deskew': ((c_double,), MagickBoolean),
                'trim': ((c_double,), MagickBoolean),
                'splice': ((c_size_t, c_size_t, c_ssize_t, c_ssize_t), MagickBoolean),
                
                'brightness_contrast': ((c_double, c_double), MagickBoolean),
                'gamma': ((c_double,), MagickBoolean),
                'auto_gamma': ((), MagickBoolean),
                'auto_level': ((), MagickBoolean),
                'modulate': ((c_double, c_double, c_double), MagickBoolean),
                'sepia_tone': ((c_double,), MagickBoolean),
                'equalize': ((), MagickBoolean),
                'negate': ((MagickBoolean,), MagickBoolean),
                'solarize': ((c_double,), MagickBoolean),
                'posterize': ((c_uint, MagickBoolean), MagickBoolean),
                
                'blur': ((c_double, c_double), MagickBoolean),
                'radial_blur': ((c_double,), MagickBoolean),
                'enhance': ((), MagickBoolean),
                'despeckle': ((), MagickBoolean),
                'emboss': ((c_double, c_double), MagickBoolean),
                
                'swirl': ((c_double,), MagickBoolean),
                'wave': ((c_double, c_double), MagickBoolean),
                
                'sketch': ((c_double, c_double, c_double), MagickBoolean),
                'oil_paint': ((c_double,), MagickBoolean),
                'spread': ((c_double,), MagickBoolean),
                'forward_fourier_transform': ((MagickBoolean,), MagickBoolean),
                'fx': ((c_char_p,), MagickWand_p),
                
                'colorize': ((PixelWand_p, PixelWand_p), MagickBoolean),
                ('set', 'color'): ((PixelWand_p,), MagickBoolean),
                ('set', 'opacity'): ((c_double,), MagickBoolean),
                'composite': ((MagickWand_p, enum, c_ssize_t, c_ssize_t), MagickBoolean),
                
                'next': ((), MagickBoolean)
            } 
        },
            
        'pixel' : {
            'format': pixel_format,
            'arg': PixelWand_p,
            'symbols': {
                'set_red': ((c_double,),),
                'get_red': ((), c_double),
                'set_green': ((c_double,),),
                'get_green': ((), c_double),
                'set_blue': ((c_double,),),
                'get_blue': ((), c_double),
                'set_alpha': ((c_double,),),
                'get_alpha': ((), c_double),
                'set_color': ((c_char_p,), MagickBoolean),
                'get_hsl': ((POINTER(c_double), POINTER(c_double), POINTER(c_double)),)
            }
        }
    }


@memoized
def get_bridge():
    if environ.get('PYSTACIA_IMPL', '').upper() == 'SIMPLE':
        logger.debug('Using Simple implementation')
        impl = SimpleImpl()
    else:
        logger.debug('Using Thread implementation')
        impl = ThreadImpl(True)
        
    bridge = CallBridge(impl)
    
    return bridge


def call(callable_, *args, **kw):
    bridge = get_bridge()
    
    return bridge.call(callable_, *args, **kw)


def simple_call(obj, method, *args, **kw):
    return call(lambda: c_call(obj, method, *args, **kw))

def get_c_method(obj, method, throw=True):
    if hasattr(obj.__class__, '_api_type'):
        api_type = obj.__class__._api_type
    else:
        api_type = obj
        
    msg = formattable('Translating method {0}.{1}')
    logger.debug(msg.format(api_type, method))
    
    type_data = get_data()[api_type]
    method_name = type_data['format'](method)
    
    if not throw and not hasattr(get_dll(False), method_name):
        return False
    
    c_method = getattr(get_dll(False), method_name)
    
    if c_method.argtypes == None:
        msg = formattable('Annoting {0}')
        logger.debug(msg.format(method_name))
        method_data = type_data['symbols'][method]
        
        argtypes = method_data[0]
        if 'arg' in type_data:
            argtypes = (type_data['arg'],) + argtypes
        c_method.argtypes = argtypes
        
        restype = type_data.get('result')
        if len(method_data) == 2:
            restype = method_data[1]
        c_method.restype = restype
        
    return method_name, c_method


def c_call(obj, method, *args, **kw):
    method_name, c_method = get_c_method(obj, method)
    
    try:
        init = kw.pop('__init')
    except KeyError:
        init = True
    
    if init:
        get_dll()
    
    msg = formattable('Calling {0}')
    logger.debug(msg.format(method_name))
    
    if isinstance(obj, Resource):
        args = (obj,) + args
    
    args_ = []
    for arg, type in zip(args, c_method.argtypes):  # @ReservedAssignment
        if isinstance(arg, Resource):
            arg = arg.resource
        elif type == c_char_p:
            arg = b(arg)
            
        args_.append(arg)
    
    result = c_method(*args_)
    
    if c_method.restype == c_char_p:
        result = native_str(result)
    elif c_method.restype == enum:
        result = result.value
    elif c_method.restype == MagickBoolean and not result.value:
        exc_type = ExceptionType()
        description = c_call('magick', 'get_exception', args_[0], exc_type)
        try:
            raise PystaciaException(native_str(string_at(description)))
        finally:
            c_call('magick_', 'relinquish_memory', description)
    
    return result

from os import environ 
from ctypes import (string_at, c_char_p, c_void_p, POINTER,
                    c_size_t, c_double, c_uint)

from six import string_types, b

from pystacia.util import PystaciaException
from pystacia.compat import native_str, formattable, c_ssize_t
from pystacia.api import get_dll 
from pystacia.api.enum import (lookup as enum_lookup,
                               reverse_lookup as reverse_enum_lookup)
from pystacia.bridge import CallBridge, ThreadImpl, SimpleImpl
from pystacia.common import Resource
from pystacia import logger
from pystacia.api.type import (
    MagickWand_p, PixelWand_p, MagickBoolean, ExceptionType, enum)
