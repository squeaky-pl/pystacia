def get_pixel(self, x, y, factory=None):
    if not factory:
        factory = Color
    
    color_ = factory()
    
    c_call(self, ('get', 'pixel_color'), x, y, color_)
    
    return color_


def fill(image, fill, blend):
        # image magick ignores alpha setting of color
        # let's incorporate it into blend
        blend *= fill.alpha
        
        blend = from_rgb(blend, blend, blend)
        
        c_call(image, 'colorize', fill, blend)


def set_color(image, fill):
    if get_c_method(image, ('set', 'color')):
        c_call(image, ('set', 'color'), fill)
        
        # MagickSetImageColor doesnt copy alpha
        if not fill.opaque:
            set_alpha(image, fill.alpha)
    else:
        width, height = image.size
        image._free()
        image.__init__(blank(width, height, fill)._claim())


def set_alpha(image, alpha):
    c_call(image, ('set', 'opacity'), alpha)


def overlay(image, other, x, y, composite):
    if not composite:
        composite = composites.over
        
    composite = enum_lookup(composite)
    
    c_call(image, 'composite', other, composite, x, y)
        
from pystacia.api.func import get_c_method, c_call
from pystacia.api.enum import lookup as enum_lookup
from pystacia.image import composites, blank
from pystacia.color import from_rgb, Color