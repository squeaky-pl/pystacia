# coding: utf-8

# pystacia/image/_impl/deform.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


def swirl(image, angle):
    c_call(image, 'swirl', angle)


def wave(image, amplitude, length, offset, axis):
    if not axis:
        axis = axes.x

    transparent = from_string('transparent')

    # preserve background color
    old_color = Color()

    c_call(image, ('get', 'background_color'), old_color)
    c_call(image, ('set', 'background_color'), transparent)

    c_call(image, 'wave', amplitude, length)

    c_call(image, ('set', 'background_color'), old_color)


from pystacia.api.func import c_call
from pystacia.color import from_string, Color
from pystacia.image.enum import axes
