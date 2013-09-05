from os.path import dirname, join

from pystacia import (
    lena, magick_logo, rose, wizard, granite, netscape, filters)

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.write(join(dest, 'lena.jpg'))
image.close()

image = lena(128)
image.write(join(dest, 'lena128.jpg'))
image.close()

image = magick_logo()
image.write(join(dest, 'magick_logo.jpg'))
image.close()

image = rose()
image.write(join(dest, 'rose.jpg'))
image.close()

image = wizard()
image.write(join(dest, 'wizard.jpg'))
image.close()

image = granite()
image.write(join(dest, 'granite.jpg'))
image.close()

image = netscape()
image.write(join(dest, 'netscape.jpg'))
image.close()


def closeup(f=None, factor=4):
    image = lena()
    image.resize(32, 32, 256, 256)

    if f:
        f(image)

    image.rescale(factor=factor, filter=filters.point)

    return image


image = closeup()
image.write(join(dest, 'lena_closeup.jpg'))
image.close()

import generic

import colorspace
import type
import trim

import rescale
import resize
import rotate
import flip
import trans
import skew
import roll
import straighten

import contrast
import brightness
import gamma
import modulate
import desaturate
import colorize
import sepia
import equalize
import invert
import solarize
import posterize

import blur
import radial_blur
import denoise
import despeckle
import emboss

import swirl
import wave

import sketch
import oil_paint
import spread
import fx

import fill
import set_color
import set_alpha
import overlay
