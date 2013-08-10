from ctypes import c_char_p, c_void_p, POINTER, c_size_t, c_double, c_uint

from six import string_types

from pystacia.api.type import (
    MagickWand_p, PixelWand_p, MagickBoolean, enum, ExceptionType)
from pystacia.api.compat import c_ssize_t
from pystacia.util import PystaciaException

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
    elif hasattr(name, '__getitem__') and len(name) == 3:
        return 'Magick' + name[0].title() + name[2].title()
    else:
        raise PystaciaException('Incorrect name format')

    return ('Magick' + ''.join(x.title() for x in verb.split('_')) +
            'Image' + ''.join(x.title() for x in noun.split('_')))


def pixel_format(name):
    if name == 'get_hsl':
        name = 'GetHSL'
    elif name == 'set_hsl':
        name = 'SetHSL'
    else:
        name = ''.join(x.title() for x in name.split('_'))
    return 'Pixel' + name


data = {
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
            'ping': ((ch,), b),
            ('ping', 'blob'): ((ch, s), b),
            ('read', 'blob'): ((ch, s), b),
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
            'sharpen': ((d, d, d), b),
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
            'get_hsl': ((P(d), P(d), P(d)),),
            'set_hsl': ((d, d, d),),
            'get_exception': ((P(ExceptionType),), v)
        }
    }
}
