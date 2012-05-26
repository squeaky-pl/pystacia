# coding: utf-8

# pystacia/api/type.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.api.compat import c_void_p, c_int


class enum(c_int):
    pass


class MagickBoolean(enum):
    pass


class ExceptionType(enum):
    pass


class MagickWand_p(c_void_p):
    pass


class PixelWand_p(c_void_p):
    pass
