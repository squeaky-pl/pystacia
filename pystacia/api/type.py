# coding: utf-8
# pystacia/api/type.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from ctypes import Structure, POINTER, c_int


class enum(c_int):
    pass


class MagickBoolean(enum):
    pass


class ExceptionType(enum):
    pass


class MagickWand(Structure):
    pass
MagickWand_p = POINTER(MagickWand)


class PixelWand(Structure):
    pass
PixelWand_p = POINTER(PixelWand)
