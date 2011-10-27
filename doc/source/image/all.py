from tinyimg import lena, filters


image = lena(256)
image.write('../_static/generated/lena.jpg')
image.close()

image = lena(128)
image.write('../_static/generated/lena128.jpg')
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
import modulate
import desaturate