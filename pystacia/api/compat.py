# coding: utf-8

# pystacia/api/compat.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from ctypes import c_char_p, c_void_p, c_size_t, c_double, c_uint, c_int, byref

from pystacia.compat import jython


if jython:
    from pystacia.api.jnatypes import POINTER, find_library, string_at, CDLL
else:
    from ctypes import POINTER, string_at, CDLL #@UnusedImport
    from ctypes.util import find_library  # @UnusedImport
    c_void = None

    try:
        from ctypes import c_ssize_t  # @UnusedImport
    except ImportError:
        # python <=2.6 doesnt have c_ssize_t,
        # implementation copied from ctypes from 2.7
        from ctypes import (c_long, c_longlong,
                                sizeof, c_uint, c_ulong, c_ulonglong)

        if sizeof(c_uint) == sizeof(c_void_p):
            c_ssize_t = c_int
        elif sizeof(c_ulong) == sizeof(c_void_p):
            c_ssize_t = c_long
        elif sizeof(c_ulonglong) == sizeof(c_void_p):
            c_ssize_t = c_longlong
