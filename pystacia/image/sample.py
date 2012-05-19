# coding: utf-8

# pystacia/image/sample.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import with_statement

import sys
from os.path import dirname, join, exists
from threading import Lock
import weakref


__lena = None
__lock = Lock()


def __lena_image(factory=None):
    """Perform weakref memoization of Lena."""
    global __lena

    lena_path = join(dirname(pystacia.__file__), 'lena.png')
    if not exists(lena_path) or 'png' not in magick.get_formats():
        raise PystaciaException('Not available')

    if not __lena:
        with __lock:
            if not __lena:
                lena = io.read(lena_path, factory)
                __lena = weakref.ref(lena)
    else:
        lena = __lena()
        if not lena:
            with __lock:
                if not lena:
                    lena = io.read(lena_path, factory)
                    __lena = weakref.ref(lena)

    return lena.copy()

from pystacia.util import memoized


@memoized
def lena_available():
    """Check if lena test image is available in this intall

        Returns ``True`` if Lena test image is available i.e. ImageMagick
        is compiled with support for
        :term:`PNG` format and :term:`PNG` file can be located.
    """
    try:
        __lena_image()
    except PystaciaException:
        e = sys.exc_info()[1]
        if e.args[0] == 'Not available':
            return False

        raise

    return True


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

    img.convert_colorspace(colorspaces.rgb)

    return img


def magick_logo(factory=None):
    """Return ImageMagick logo image.

       Resulting image is 640x480, palette, RGB colorspace image.
    """
    return io.read('logo:', factory=factory)


def rose(factory=None):
    """Return rose image.

       Resulting image is 70x48, RGB, truecolor.
    """
    return io.read('rose:', factory=factory)


def wizard(factory=None):
    """Return wizard image.

       Resulting image is 480x640, palette, RGB image.
    """
    return io.read('wizard:', factory=factory)


def granite(factory=None):
    """Return granite texture.

       Resulting image is 128x128 pallette, RGB image.
    """
    return io.read('granite:', factory=factory)


def netscape(factory=None):
    """Return standard Netscape 216 color cube.

       Color cube also known as "Websafe Colors".
       216x144, palette, RGB.
    """
    return io.read('netscape:', factory=factory)

import pystacia
from pystacia.image._impl import io
from pystacia.image.enum import colorspaces
from pystacia import magick
from pystacia.util import PystaciaException
