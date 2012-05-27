# coding: utf-8

# pystacia/magick/_impl.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


def get_options():
    options = {}

    size = c_size_t()
    keys = c_call('magick_', 'query_configure_options', '*', byref(size))
    for key in [native_str(keys[i]) for i in range(size.value)]:
        options[key] = (
        c_call('magick_', 'query_configure_option', key))

    return options


def get_formats():
    size = c_size_t()
    formats = c_call('magick_', 'query_formats', '*', byref(size))

    return [native_str(formats[i]).lower() for i in range(size.value)]

from pystacia.compat import native_str
from pystacia.api.func import c_call
from pystacia.api.compat import c_size_t, byref
