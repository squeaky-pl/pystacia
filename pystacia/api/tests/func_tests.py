# coding: utf-8
# pystacia/api/tests/func_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.compat import TestCase


class Guard(TestCase):
    def test(self):
        img = lena()
        
        ccall = lambda: cdll.MagickSetFormat(img.wand, b('lolz'))
        self.assertRaises(TinyException, lambda: guard(img.wand, ccall))
        
        guard(img.wand, lambda: cdll.MagickSetFormat(img.wand, b('bmp')))
        
        img.close()


from six import b

from pystacia import lena, cdll
from pystacia.api.func import guard
from pystacia.util import TinyException
