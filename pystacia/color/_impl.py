# coding: utf-8

# pystacia/color/_impl.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from ctypes import c_double


def alloc():
    return c_call('pwand', 'new')


def free(color):
    return c_call('pwand', 'destroy', color)


def clone(color):
    return c_call('pwand', 'clone', color)


def set_string(color, value):
    c_call(color, 'set_color', value)


def get_red(color):
    return saturate(c_call(color, 'get_red'))


def set_red(color, value):
    c_call(color, 'set_red', value)


def get_green(color):
    return saturate(c_call(color, 'get_green'))


def set_green(color, value):
    c_call(color, 'set_green', value)


def get_blue(color):
    return saturate(c_call(color, 'get_blue'))


def set_blue(color, value):
    c_call(color, 'set_blue', value)


def get_alpha(color):
    return saturate(c_call(color, 'get_alpha'))


def set_alpha(color, value):
    c_call(color, 'set_alpha', value)


def get_hsl(color):
    h, s, l = tuple(x() for x in (c_double,) * 3)

    c_call(color, 'get_hsl', h, s, l)

    return tuple(saturate(x.value) for x in (h, s, l))


def set_hsl(color, hue, saturation, lightness):
    c_call(color, 'set_hsl', hue, saturation, lightness)


def saturate(v):
    if v == 0:
        return 0
    elif v == 1:
        return 1
    else:
        return round(v, 4)


from pystacia.api.func import c_call
