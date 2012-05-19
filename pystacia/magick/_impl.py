# coding: utf-8
# pystacia/magick/_impl.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from ctypes import c_size_t


def get_options():
    options = {}

    size = c_size_t()
    keys = c_call('magick_', 'query_configure_options', '*', size)
    for key in (native_str(keys[i]) for i in range(size.value)):
        options[key] = (
        c_call('magick_', 'query_configure_option', key))

    return options


def get_formats():
    size = c_size_t()
    formats = c_call('magick_', 'query_formats', '*', size)

    return [native_str(formats[i]).lower() for i in range(size.value)]

from pystacia.api.func import c_call
from pystacia.compat import native_str
