# coding: utf-8
# pystacia/__init__.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""pystacia is a raster graphics library utilizing ImageMagick."""


from logging import getLogger

logger = getLogger('pystacia')


__lena = None


def __lena_image(factory=None):
    """Perform weakref memoization of Lena."""
    global __lena
    
    if not __lena:
        lena = image.read(__lena_path)
        __lena = weakref.ref(lena)
    else:
        lena = __lena()
        if not lena:
            lena = image.read(__lena_path)
            __lena = weakref.ref(lena)
    
    return lena.copy()


def lena(width=None, factory=None):
    """Return standard lena test image.
       
       Resulting :class:`.Image` object is a TrueType in, RGB colorspace,
       8bit per channel image. For background on the test image see:
       http://en.wikipedia.org/wiki/Lenna.
       
       :param width: Returned image will be of this size. When not specified
         defaults to 512x512 which is how the bitmap is stored internally.
       
    """
    img = __lena_image(factory)
    
    if width:
        img.rescale(width, width)

    img.convert_colorspace(image.colorspaces.rgb)
        
    return img


def magick_logo(factory=None):
    """Return ImageMagick logo image.
        
       Resulting image is 640x480, palette, RGB colorspace image.
    """
    return image.read_special('logo:', factory=factory)


def rose(factory=None):
    """Return rose image.
    
       Resulting image is 70x48, RGB, truecolor.
    """
    return image.read_special('rose:', factory=factory)


def wizard(factory=None):
    """Return wizard image.
    
       Resulting image is 480x640, palette, RGB image.
    """
    return image.read_special('wizard:', factory=factory)


def granite(factory=None):
    """Return granite texture.
    
       Resulting image is 128x128 pallette, RGB image.
    """
    return image.read_special('granite:', factory=factory)


def netscape(factory=None):
    """Return standard Netscape 216 color cube.
       
       Color cube also known as "Websafe Colors".
       216x144, palette, RGB.
    """
    return image.read_special('netscape:', factory=factory)

cdll = None

import weakref
from os.path import dirname, join, exists

from pystacia.compat import formattable
from pystacia.util import PystaciaException
from pystacia import common

from pystacia import magick
#from pystacia import image

#convenience imports
#from pystacia.image import read, read_blob, read_raw
#from pystacia.image import blank, checkerboard
#from pystacia.image import (
#    composites, types, filters, colorspaces, compressions, axes)
from pystacia import color
#from pystacia.image import Image


colors = color.Factory()
"""Convenience factory for SVG names"""

__lena_path = join(dirname(__file__), 'lena.png')

#if not exists(__lena_path) or 'png' not in magick.get_delegates():
#    del lena

#__all__ = [
#    'magick_logo', 'rose', 'wizard', 'granite', 'netscape',
#    'read', 'read_blob', 'read_raw',
#    'blank', 'checkerboard',
#    'composites', 'types', 'filters', 'colorspaces', 'compressions', 'axes',
#    'color', 'colors',
#    'Image']

#if globals().get('lena'):
#    __all__.append('lena')
