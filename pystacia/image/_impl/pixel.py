# coding: utf-8

# pystacia/image/_impl/pixel.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


def get_pixel(self, x, y, factory):
    color_ = color._instantiate(factory)

    c_call(self, ('get', 'pixel_color'), x, y, color_)

    return color_


def fill(image, fill, blend):
    # image magick ignores alpha setting of color
    # let's incorporate it into blend
    blend *= fill.alpha

    blend = from_rgb(blend, blend, blend)

    c_call(image, 'colorize', fill, blend)


def set_color(image, fill):
    if get_c_method(image, ('set', 'color'), throw=False):
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

    composite = enum_lookup(composite, composites)

    c_call(image, 'composite', other, composite, x, y)


def compare(image, other, metric, factory):
    if image.size != other.size:
        return False

    if not metric:
        metric = metrics.absolute_error

    metric = enum_lookup(metric, metrics)

    if not factory:
        factory = Image

    distortion = c_double()

    diff = c_call(image, ('compare', None, 'images'), other,
                  metric, byref(distortion))

    return(factory(diff), distortion.value)


from pystacia.api.func import get_c_method, c_call
from pystacia.api.enum import lookup as enum_lookup
from pystacia.api.compat import c_double, byref
from pystacia.image.enum import metrics, composites
from pystacia.image import Image
from pystacia.image.generic import blank
from pystacia.color import from_rgb
from pystacia import color
