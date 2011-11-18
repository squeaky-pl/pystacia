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
    b = MagickBoolean  # @Reimport
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
        elif hasattr(name, '__getitem__') and len(name) == 3:
            return 'Magick' + name[0].title() + name[2].title()
        else:
            raise PystaciaException('Incorrect name format')
        
        return ('Magick' + ''.join(x.title() for x in verb.split('_')) +
                'Image' + ''.join(x.title() for x in noun.split('_')))
    
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
            'arg': w,
            'symbols': {
                'set_size': ((s, s), b),
                'get_format': ((), ch),
                'set_format': ((ch,), b),
                'set_depth': ((s,), b),
                'get_exception': ((P(ExceptionType),), v)
            }
        },
        
        'magick_': {
            'format': magick_format,
            'symbols': {
                'query_configure_options': ((ch, P(s)), P(ch)),
                'query_configure_option': ((ch,), ch),
                'query_formats': ((ch, P(s)), P(ch)),
                'get_version': ((P(s),), ch),
                'relinquish_memory': ((v,), v)
            }
        },
        
        'wand': {
            'format': lambda name: name.title() + 'MagickWand',
            'result': w,
            'symbols': {
                'new': ((),),
                'clone': ((w,),),
                'destroy': ((w,),)
            }
        },
        
        'pwand': {
            'format': lambda name: name.title() + 'PixelWand',
            'result': pw,
            'symbols': {
                'new': ((),),
                'clone': ((pw,),),
                'destroy': ((pw,),)
            }
        },
        
        'image': {
            'format': image_format,
            'arg': w,
            'symbols': {
                'read': ((ch,), b),
                'write': ((ch,), b),
                ('read', 'blob'): ((v, s), b),
                ('get', 'blob'): ((P(s),), v),
                
                ('set', 'format'): ((ch,), b),
                ('get', 'format'): ((), ch),
                ('set', 'compression_quality'): ((s,), b),
                ('get', 'compression_quality'): ((), s),
                ('get', 'width'): ((), s),
                ('get', 'height'): ((), s),
                ('get', 'depth'): ((), s),
                ('set', 'depth'): ((s,), b),
                ('get', 'type'): ((), e),
                ('set', 'type'): ((e,), b),
                ('get', 'colorspace'): ((), e),
                ('set', 'colorspace'): ((e,), b),
                ('get', 'pixel_color'): ((ss, ss, pw),
                                         b),
                ('set', 'background_color'): ((pw,), b),
                ('get', 'background_color'): ((pw,), b),
                ('transform', 'colorspace'): ((e,), b),
                
                'resize': ((s, s, e, d), b),
                'crop': ((s, s, ss, ss), b),
                'rotate': ((pw, d), b),
                'flip': ((), b),
                'flop': ((), b),
                'transpose': ((), b),
                'transverse': ((), b),
                'shear': ((pw, d, d), b),
                'roll': ((ss, ss), b),
                'deskew': ((d,), b),
                'trim': ((d,), b),
                'splice': ((s, s, ss, ss), b),
                'chop': ((s, s, ss, ss), b),
                
                'brightness_contrast': ((d, d), b),
                'gamma': ((d,), b),
                'auto_gamma': ((), b),
                'auto_level': ((), b),
                'modulate': ((d, d, d), b),
                'sepia_tone': ((d,), b),
                'equalize': ((), b),
                'normalize': ((), b),
                'negate': ((b,), b),
                'solarize': ((d,), b),
                'posterize': ((u, b), b),
                'clut': ((w, e), b),
                'threshold': ((d,), b),
                'black_threshold': ((pw,), b),
                'white_threshold': ((pw,), b),
                'random_threshold': ((d, d), b),
                'contrast_stretch': ((d, d), b),
                'evaluate': ((e, d), b),
                ('get', 'colors'): ((), s),
                ('get', 'range'): ((P(d), P(d)), b),
                
                'blur': ((d, d), b),
                'gaussian_blur': ((d, d, d), b),
                'motion_blur': ((d, d, d, d), b),
                'edge': ((d, d), b),
                'adaptive_blur': ((d, d, d), b),
                'adaptive_sharpen': ((d, d, d), b),
                'radial_blur': ((d,), b),
                'enhance': ((), b),
                'despeckle': ((), b),
                'emboss': ((d, d), b),
                
                'swirl': ((d,), b),
                'wave': ((d, d), b),
                
                'sketch': ((d, d, d), b),
                'add_noise': ((e, d), b),
                'charcoal': ((d, d, d), b),
                'oil_paint': ((d,), b),
                'spread': ((d,), b),
                'forward_fourier_transform': ((b,), b),
                'fx': ((ch,), w),
                'shade': ((b, d, d), b),
                
                'colorize': ((pw, pw), b),
                ('set', 'color'): ((pw,), b),
                ('set', 'opacity'): ((d,), b),
                'composite': ((w, e, ss, ss), b),
                ('compare', None, 'images'): ((w, e, P(d)), w),
                
                'next': ((), b)
            }
        },
        
        'pixel': {
            'format': pixel_format,
            'arg': pw,
            'symbols': {
                'set_red': ((d,),),
                'get_red': ((), d),
                'set_green': ((d,),),
                'get_green': ((), d),
                'set_blue': ((d,),),
                'get_blue': ((), d),
                'set_alpha': ((d,),),
                'get_alpha': ((), d),
                'set_color': ((ch,), b),
                'get_hsl': ((P(d), P(d), P(d)),)
            }
        }
    }


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
        elif type == PixelWand_p:
            arg = color_cast(arg)
            
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


from ctypes import (string_at, c_char_p, c_void_p, POINTER,
                    c_size_t, c_double, c_uint)

from six import string_types, b

from pystacia.util import PystaciaException
from pystacia.compat import native_str, formattable, c_ssize_t
from pystacia.api import get_dll, get_bridge, logger
from pystacia.api.type import (
    MagickWand_p, PixelWand_p, MagickBoolean, ExceptionType, enum)
from pystacia.common import Resource
from pystacia.color import cast as color_cast
