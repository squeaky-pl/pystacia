# coding: utf-8

# pystacia/image/_impl/special.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


def sketch(image, radius, angle, strength):
    if strength is None:
        strength = radius

    c_call(image, 'sketch', radius, strength, angle)


def add_noise(image, attenuate, noise_type):
    if not noise_type:
        noise_type = 'gaussian'

    noise_type = enum_lookup(noise_type, noises)

    c_call(image, 'add_noise', noise_type, attenuate)


def oil_paint(image, radius):
    c_call(image, 'oil_paint', radius)


def charcoal(image, radius, strength, bias):
    if strength is None:
        strength = radius
    if bias is None:
        bias = 0

    c_call(image, 'charcoal', radius, strength, bias)


def shade(image, azimuth, elevation, grayscale):
    c_call(image, 'shade', grayscale, azimuth, elevation)


def spread(image, radius):
    c_call(image, 'spread', radius)


def fx(image, expression):
    resource = c_call(image, 'fx', expression)

    image._free()
    image.__init__(resource)

from pystacia.api.func import c_call
from pystacia.image.enum import noises
from pystacia.api.enum import lookup as enum_lookup
