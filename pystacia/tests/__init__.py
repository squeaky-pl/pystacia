# coding: utf-8
# pystacia/tests/__init__.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia import image
from pystacia.image import types
from pystacia.image.sample import lena_available


if lena_available():
    sample = image.lena
    sample.size = (512, 512)
    sample.type = types.truecolor
else:
    sample = image.magick_logo
    sample.size = (640, 480)
    sample.type = types.palette

from pystacia.tests.common import TestCase, skipIf

class MagickLogo(TestCase):
    def test(self):
        img = image.magick_logo()
        
        self.assertEquals(img.size, (640, 480))
        self.assertEquals(img.type, types.palette)


class Lena(TestCase):
    @skipIf(not lena_available(), 'Lena not available')
    def test(self):
        img = image.lena()
        self.assertEquals(img.size, (512, 512))
        self.assertEquals(img.type, types.truecolor)
        self.assertEquals(img.colorspace, colorspaces.rgb)
        img.close()
        
        img = image.lena(32)
        self.assertEquals(img.size, (32, 32))
        self.assertEquals(img.colorspace, colorspaces.rgb)
        img.close()


class DeprecationTest(TestCase):
    def test(self):
        import pystacia
        from pystacia import image
        
        with catch_warnings(record=True) as w:
            simplefilter('always')
            
            self.assertTrue(image.blank(30, 30).
                            is_same(pystacia.blank(30, 30)))
            
            if lena_available():
                self.assertTrue(image.lena().is_same(pystacia.lena()))
            
            for sample in ['magick_logo', 'wizard',
                           'netscape', 'granite', 'rose']:
                self.assertTrue(getattr(image, sample)().
                                is_same(getattr(pystacia, sample)()))
                
            self.assertIsInstance(pystacia.Image(), image.Image)
            
        with catch_warnings(record=True) as w:
            simplefilter('always')
            names = ['composites', 'types', 'filters', 'colorspaces',
                     'compressions', 'axes']
            for name in names:
                self.assertEquals(getattr(pystacia, name).x,
                                  getattr(image, name).x)


from pystacia.image import colorspaces
from warnings import catch_warnings, simplefilter
