# coding: utf-8
# pystacia/tests/__init__.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import pystacia
from pystacia.image import types


if hasattr(pystacia, 'lena'):
    sample = pystacia.lena
    sample.size = (512, 512)
    sample.type = types.truecolor
else:
    sample = pystacia.magick_logo
    sample.size = (640, 480)
    sample.type = types.palette


from pystacia.compat import TestCase, skipIf


class MagickLogo(TestCase):
    def test(self):
        img = pystacia.magick_logo()
        
        self.assertEquals(img.size, (640, 480))
        self.assertEquals(img.type, types.palette)


class Lena(TestCase):
    @skipIf(not hasattr(pystacia, 'lena'), 'Lena not available')
    def test(self):
        img = pystacia.lena()
        self.assertEquals(img.size, (512, 512))
        self.assertEquals(img.type, types.truecolor)
        self.assertEquals(img.colorspace, colorspaces.rgb)
        img.close()
        
        img = pystacia.lena(32)
        self.assertEquals(img.size, (32, 32))
        self.assertEquals(img.colorspace, colorspaces.rgb)
        img.close()


from pystacia.image import colorspaces
