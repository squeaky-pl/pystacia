# coding: utf-8
# pystacia/api/enum.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

data =\
{'colorspace': [{'_version': (6, 5, 9, 0),
                 'cmy': 22,
                 'cmyk': 12,
                 'gray': 2,
                 'hsb': 14,
                 'hsl': 15,
                 'hwb': 16,
                 'lab': 5,
                 'log': 21,
                 'ohta': 4,
                 'rec601luma': 17,
                 'rec601ycbcr': 18,
                 'rec709luma': 19,
                 'rec709ycbcr': 20,
                 'rgb': 1,
                 'srgb': 13,
                 'transparent': 3,
                 'undefined': 0,
                 'xyz': 6,
                 'ycbcr': 7,
                 'ycc': 8,
                 'yiq': 9,
                 'ypbpr': 10,
                 'yuv': 11}],
 'composite': [{'_version': (6, 5, 9, 0),
                'atop': 3,
                'blend': 4,
                'blur': 57,
                'bumpmap': 5,
                'change_mask': 6,
                'clear': 7,
                'color_burn': 8,
                'color_dodge': 9,
                'colorize': 10,
                'copy': 13,
                'copy_black': 11,
                'copy_blue': 12,
                'copy_cyan': 14,
                'copy_green': 15,
                'copy_magenta': 16,
                'copy_opacity': 17,
                'copy_red': 18,
                'copy_yellow': 19,
                'darken': 20,
                'difference': 26,
                'displace': 27,
                'dissolve': 28,
                'distort': 56,
                'divide_dst': 55,
                'dst': 22,
                'dst_atop': 21,
                'dst_in': 23,
                'dst_out': 24,
                'dst_over': 25,
                'exclusion': 29,
                'hard_light': 30,
                'hue': 31,
                'in': 32,
                'lighten': 33,
                'linear_burn': 62,
                'linear_dodge': 61,
                'linear_light': 34,
                'luminize': 35,
                'mathematics': 63,
                'minus_dst': 36,
                'modulate': 37,
                'modulus_add': 2,
                'modulus_subtract': 52,
                'multiply': 38,
                'no': 1,
                'out': 39,
                'over': 40,
                'overlay': 41,
                'pegtop_light': 58,
                'pin_light': 60,
                'plus': 42,
                'replace': 43,
                'saturate': 44,
                'screen': 45,
                'soft_light': 46,
                'src': 48,
                'src_atop': 47,
                'src_in': 49,
                'src_out': 50,
                'src_over': 51,
                'threshold': 53,
                'undefined': 0,
                'vivid_light': 59,
                'xor': 54},
               {'_version': (6, 6, 8, 6),
                'atop': 3,
                'blend': 4,
                'blur': 57,
                'bumpmap': 5,
                'change_mask': 6,
                'clear': 7,
                'color_burn': 8,
                'color_dodge': 9,
                'colorize': 10,
                'copy': 13,
                'copy_black': 11,
                'copy_blue': 12,
                'copy_cyan': 14,
                'copy_green': 15,
                'copy_magenta': 16,
                'copy_opacity': 17,
                'copy_red': 18,
                'copy_yellow': 19,
                'darken': 20,
                'difference': 26,
                'displace': 27,
                'dissolve': 28,
                'distort': 56,
                'divide_dst': 55,
                'divide_src': 64,
                'dst': 22,
                'dst_atop': 21,
                'dst_in': 23,
                'dst_out': 24,
                'dst_over': 25,
                'exclusion': 29,
                'hard_light': 30,
                'hue': 31,
                'in': 32,
                'lighten': 33,
                'linear_burn': 62,
                'linear_dodge': 61,
                'linear_light': 34,
                'luminize': 35,
                'mathematics': 63,
                'minus_dst': 36,
                'minus_src': 65,
                'modulate': 37,
                'modulus_add': 2,
                'modulus_subtract': 52,
                'multiply': 38,
                'no': 1,
                'out': 39,
                'over': 40,
                'overlay': 41,
                'pegtop_light': 58,
                'pin_light': 60,
                'plus': 42,
                'replace': 43,
                'saturate': 44,
                'screen': 45,
                'soft_light': 46,
                'src': 48,
                'src_atop': 47,
                'src_in': 49,
                'src_out': 50,
                'src_over': 51,
                'threshold': 53,
                'undefined': 0,
                'vivid_light': 59,
                'xor': 54},
               {'_version': (6, 6, 9, 5),
                'atop': 3,
                'blend': 4,
                'blur': 57,
                'bumpmap': 5,
                'change_mask': 6,
                'clear': 7,
                'color_burn': 8,
                'color_dodge': 9,
                'colorize': 10,
                'copy': 13,
                'copy_black': 11,
                'copy_blue': 12,
                'copy_cyan': 14,
                'copy_green': 15,
                'copy_magenta': 16,
                'copy_opacity': 17,
                'copy_red': 18,
                'copy_yellow': 19,
                'darken': 20,
                'darken_intensity': 66,
                'difference': 26,
                'displace': 27,
                'dissolve': 28,
                'distort': 56,
                'divide_dst': 55,
                'divide_src': 64,
                'dst': 22,
                'dst_atop': 21,
                'dst_in': 23,
                'dst_out': 24,
                'dst_over': 25,
                'exclusion': 29,
                'hard_light': 30,
                'hue': 31,
                'in': 32,
                'lighten': 33,
                'lighten_intensity': 67,
                'linear_burn': 62,
                'linear_dodge': 61,
                'linear_light': 34,
                'luminize': 35,
                'mathematics': 63,
                'minus_dst': 36,
                'minus_src': 65,
                'modulate': 37,
                'modulus_add': 2,
                'modulus_subtract': 52,
                'multiply': 38,
                'no': 1,
                'out': 39,
                'over': 40,
                'overlay': 41,
                'pegtop_light': 58,
                'pin_light': 60,
                'plus': 42,
                'replace': 43,
                'saturate': 44,
                'screen': 45,
                'soft_light': 46,
                'src': 48,
                'src_atop': 47,
                'src_in': 49,
                'src_out': 50,
                'src_over': 51,
                'threshold': 53,
                'undefined': 0,
                'vivid_light': 59,
                'xor': 54}],
 'compression': [{'_version': (6, 5, 9, 0),
                  'b44': 17,
                  'b44a': 18,
                  'bzip': 2,
                  'dxt1': 3,
                  'dxt3': 4,
                  'dxt5': 5,
                  'fax': 6,
                  'group4': 7,
                  'jpeg': 8,
                  'jpeg2000': 9,
                  'lossless_jpeg': 10,
                  'lzw': 11,
                  'no': 1,
                  'piz': 15,
                  'pxr24': 16,
                  'rle': 12,
                  'undefined': 0,
                  'zip': 13,
                  'zips': 14},
                 {'_version': (6, 6, 6, 6),
                  'b44': 17,
                  'b44a': 18,
                  'bzip': 2,
                  'dxt1': 3,
                  'dxt3': 4,
                  'dxt5': 5,
                  'fax': 6,
                  'group4': 7,
                  'jpeg': 8,
                  'jpeg2000': 9,
                  'lossless_jpeg': 10,
                  'lzma': 19,
                  'lzw': 11,
                  'no': 1,
                  'piz': 15,
                  'pxr24': 16,
                  'rle': 12,
                  'undefined': 0,
                  'zip': 13,
                  'zips': 14},
                 {'_version': (6, 6, 9, 7),
                  'b44': 17,
                  'b44a': 18,
                  'bzip': 2,
                  'dxt1': 3,
                  'dxt3': 4,
                  'dxt5': 5,
                  'fax': 6,
                  'group4': 7,
                  'jbig1': 20,
                  'jbig2': 21,
                  'jpeg': 8,
                  'jpeg2000': 9,
                  'lossless_jpeg': 10,
                  'lzma': 19,
                  'lzw': 11,
                  'no': 1,
                  'piz': 15,
                  'pxr24': 16,
                  'rle': 12,
                  'undefined': 0,
                  'zip': 13,
                  'zips': 14}],
 'filter': [{'_version': (6, 5, 9, 0),
             'bartlett': 21,
             'blackman': 7,
             'bohman': 20,
             'box': 2,
             'catrom': 11,
             'cubic': 10,
             'gaussian': 8,
             'hamming': 6,
             'hanning': 5,
             'hermite': 4,
             'jinc': 14,
             'kaiser': 16,
             'lagrange': 19,
             'lanczos': 13,
             'mitchell': 12,
             'parzen': 18,
             'point': 1,
             'quadratic': 9,
             'sinc': 15,
             'triangle': 3,
             'undefined': 0,
             'welsh': 17},
            {'_version': (6, 6, 4, 1),
             'bartlett': 21,
             'blackman': 7,
             'bohman': 20,
             'box': 2,
             'catrom': 11,
             'cubic': 10,
             'gaussian': 8,
             'hamming': 6,
             'hanning': 5,
             'hermite': 4,
             'jinc': 14,
             'kaiser': 16,
             'lagrange': 19,
             'lanczos': 13,
             'mitchell': 12,
             'parzen': 18,
             'point': 1,
             'quadratic': 9,
             'sinc': 15,
             'sinc_fast': 22,
             'triangle': 3,
             'undefined': 0,
             'welsh': 17},
            {'_version': (6, 6, 4, 2),
             'bartlett': 21,
             'blackman': 7,
             'bohman': 20,
             'box': 2,
             'catrom': 11,
             'cubic': 10,
             'gaussian': 8,
             'hamming': 6,
             'hanning': 5,
             'hermite': 4,
             'jinc': 14,
             'kaiser': 16,
             'lagrange': 19,
             'lanczos': 13,
             'lanczos2': 23,
             'mitchell': 12,
             'parzen': 18,
             'point': 1,
             'quadratic': 9,
             'sinc': 15,
             'sinc_fast': 22,
             'triangle': 3,
             'undefined': 0,
             'welsh': 17},
            {'_version': (6, 6, 4, 5),
             'bartlett': 21,
             'blackman': 7,
             'bohman': 20,
             'box': 2,
             'catrom': 11,
             'cubic': 10,
             'gaussian': 8,
             'hamming': 6,
             'hanning': 5,
             'hermite': 4,
             'jinc': 14,
             'kaiser': 16,
             'lagrange': 19,
             'lanczos': 13,
             'mitchell': 12,
             'parzen': 18,
             'point': 1,
             'quadratic': 9,
             'sinc': 15,
             'sinc_fast': 22,
             'triangle': 3,
             'undefined': 0,
             'welsh': 17},
            {'_version': (6, 6, 4, 10),
             'bartlett': 21,
             'blackman': 7,
             'bohman': 20,
             'box': 2,
             'catrom': 11,
             'cubic': 10,
             'gaussian': 8,
             'hamming': 6,
             'hanning': 5,
             'hermite': 4,
             'jinc': 14,
             'kaiser': 16,
             'lagrange': 19,
             'lanczos': 13,
             'lanczos2': 23,
             'mitchell': 12,
             'parzen': 18,
             'point': 1,
             'quadratic': 9,
             'robidoux': 24,
             'sinc': 15,
             'sinc_fast': 22,
             'triangle': 3,
             'undefined': 0,
             'welsh': 17},
            {'_version': (6, 6, 5, 0),
             'bartlett': 21,
             'blackman': 7,
             'bohman': 20,
             'box': 2,
             'catrom': 11,
             'cubic': 10,
             'gaussian': 8,
             'hamming': 6,
             'hanning': 5,
             'hermite': 4,
             'jinc': 14,
             'kaiser': 16,
             'lagrange': 19,
             'lanczos': 13,
             'lanczos2': 23,
             'lanczos2_sharp': 24,
             'mitchell': 12,
             'parzen': 18,
             'point': 1,
             'quadratic': 9,
             'robidoux': 25,
             'sinc': 15,
             'sinc_fast': 22,
             'triangle': 3,
             'undefined': 0,
             'welsh': 17},
            {'_version': (6, 6, 5, 4),
             'bartlett': 21,
             'blackman': 7,
             'bohman': 20,
             'box': 2,
             'catrom': 11,
             'cubic': 10,
             'gaussian': 8,
             'hamming': 6,
             'hanning': 5,
             'hermite': 4,
             'jinc': 14,
             'kaiser': 16,
             'lagrange': 19,
             'lanczos': 13,
             'lanczos2': 24,
             'lanczos2_sharp': 25,
             'lanczos_sharp': 23,
             'mitchell': 12,
             'parzen': 18,
             'point': 1,
             'quadratic': 9,
             'robidoux': 26,
             'sinc': 15,
             'sinc_fast': 22,
             'triangle': 3,
             'undefined': 0,
             'welsh': 17},
            {'_version': (6, 6, 5, 5),
             'bartlett': 20,
             'blackman': 7,
             'bohman': 19,
             'box': 2,
             'catrom': 11,
             'cubic': 10,
             'gaussian': 8,
             'hamming': 6,
             'hanning': 5,
             'hermite': 4,
             'jinc': 13,
             'kaiser': 16,
             'lagrange': 21,
             'lanczos': 22,
             'lanczos2': 24,
             'lanczos2_sharp': 25,
             'lanczos_sharp': 23,
             'mitchell': 12,
             'parzen': 18,
             'point': 1,
             'quadratic': 9,
             'robidoux': 26,
             'sinc': 14,
             'sinc_fast': 15,
             'triangle': 3,
             'undefined': 0,
             'welsh': 17}],
 'type': [{'_version': (6, 5, 9, 0),
           'bilevel': 1,
           'color_separation': 8,
           'color_separation_matte': 9,
           'grayscale': 2,
           'grayscale_matte': 3,
           'optimize': 10,
           'palette': 4,
           'palette_bilevel_matte': 11,
           'palette_matte': 5,
           'truecolor': 6,
           'truecolor_matte': 7,
           'undefined': 0}]}

from pystacia.util import memoized


@memoized
def lookup(mnemonic, version=None, throw=True):
    if not version:
        version = get_version()
        
    value = None
    
    for entry in data.get(mnemonic.enum.name, []):
        if entry['_version'] > version:
            break
        value = entry.get(mnemonic.name)
    
    if value == None and throw:
        template = "Enumeration '{enum}' cannot map mnemonic '{mnemonic}'"
        template = formattable(template)
        enum = mnemonic.enum.name
        mnemonic = mnemonic.name
        raise PystaciaException(template.format(enum=enum, mnemonic=mnemonic))
    
    return value


@memoized
def reverse_lookup(enum, value, version=None):
    mnemonic = None
    
    if not version:
        version = get_version()
    
    for entry in data.get(enum.name, []):
        if entry['_version'] > version:
            break
        lookup = dict(zip(entry.values(), entry.keys()))
        mnemonic = getattr(enum, lookup.get(value))
    
    return mnemonic

from pystacia.magick import get_version
from pystacia.util import PystaciaException
from pystacia.compat import formattable
