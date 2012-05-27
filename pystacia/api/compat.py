# coding: utf-8

# pystacia/api/compat.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from ctypes import (c_char_p, c_size_t, c_double, c_uint,  # NOQA
                    c_int, byref)
from pystacia.compat import jython


if jython:
    from ctypes import c_ssize_t  # @UnusedImport
    from pystacia.api.jnatypes import (c_void_p, POINTER, find_library,
                                      string_at, CDLL)  # @UnusedImport
else:
    from ctypes import c_void_p, POINTER, string_at, CDLL  # NOQA
    from ctypes.util import find_library  # NOQA
    c_void = None

    try:
        from ctypes import c_ssize_t  # NOQA
    except ImportError:
        # python <=2.6 doesnt have c_ssize_t,
        # implementation copied from ctypes from 2.7
        from ctypes import (c_long, c_longlong,  # NOQA
                                sizeof, c_uint, c_ulong, c_ulonglong)

        if sizeof(c_uint) == sizeof(c_void_p):
            c_ssize_t = c_int  # NOQA
        elif sizeof(c_ulong) == sizeof(c_void_p):
            c_ssize_t = c_long
        elif sizeof(c_ulonglong) == sizeof(c_void_p):
            c_ssize_t = c_longlong
