from tinyimg import lena, magick_logo, rose, wizard, granite, netscape, filters


image = lena(256)
image.write('../_static/generated/lena.jpg')
image.close()

image = lena(128)
image.write('../_static/generated/lena128.jpg')
image.close()

image = magick_logo()
image.write('../_static/generated/magick_logo.jpg')
image.close()

image = rose()
image.write('../_static/generated/rose.jpg')
image.close()

image = wizard()
image.write('../_static/generated/wizard.jpg')
image.close()

image = granite()
image.write('../_static/generated/granite.jpg')
image.close()

image = netscape()
image.write('../_static/generated/netscape.jpg')
image.close()

def closeup(f = None, factor=4):
    image = lena()
    image.resize(32, 32, 256, 256)
    
    if f:
        f(image)
    
    image.rescale(factor=factor, filter=filters.point)
    
    return image

image = closeup()
image.write('../_static/generated/lena_closeup.jpg')
image.close()

import colorspace
import type

import rescale
import resize
import rotate
import flip
import trans
import skew
import roll

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
import dft
import fx

import fill
import set_color
import set_alpha
import overlay