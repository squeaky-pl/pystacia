def brightness(image, factor):
    c_call(image, 'brightness_contrast', factor * 100, 0)


def contrast(image, factor):
    c_call(image, 'brightness_contrast', 0, factor * 100)


def gamma(image, gamma):
    c_call(image, 'gamma', gamma)


def auto_gamma(image):
    c_call(image, 'auto_gamma')


def auto_level(image):
    c_call(image, 'auto_level')


def modulate(image, hue, saturation, lightness):
    c_call(image, 'modulate', lightness * 100 + 100, saturation * 100 + 100,
                              hue * 100 + 100)


def sepia(image, threshold, saturation):
    threshold = (2 ** magick.get_depth() - 1) * threshold
    
    c_call(image, 'sepia_tone', threshold)
    
    if saturation:
        modulate(image, 0, saturation, 0)


def equalize(image):
    c_call(image, 'equalize')


def invert(image, only_gray):
    c_call(image, 'negate', only_gray)


def solarize(image, factor):
    factor = (1 - factor) * (2 ** magick.get_depth() - 1)
    
    c_call(image, 'solarize', factor)


def posterize(image, levels, dither=False):
    c_call(image, 'posterize', levels, dither)


def convert_colorspace(image, colorspace):
    colorspace = enum_lookup(colorspace)
    c_call(image, ('transform', 'colorspace'), colorspace)


from pystacia import magick
from pystacia.api.func import c_call
from pystacia.api.enum import lookup as enum_lookup