# coding: utf-8
# pystacia/tests/__init__.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import with_statement

from pystacia.tests.common import TestCase, skipIf
from pystacia.image.sample import lena_available


class Lena(TestCase):
    @skipIf(not lena_available(), 'Lena not available')
    def test(self):
        img = image.lena()
        self.assertEqual(img.size, (512, 512))
        self.assertEqual(img.type, types.truecolor)
        self.assertEqual(img.colorspace, colorspaces.rgb)
        img.close()
        
        img = image.lena(32)
        self.assertEqual(img.size, (32, 32))
        self.assertEqual(img.colorspace, colorspaces.rgb)
        img.close()

from sys import version_info


class DeprecationTest(TestCase):
    @skipIf(version_info < (2, 6), 'Catching warnings not available')
    def test(self):
        import pystacia
        from pystacia import image
        
        with catch_warnings(record=True) as w:
            simplefilter('always')
            
            self.assertTrue(image.blank(30, 30).
                            is_same(pystacia.blank(30, 30)))
            
            self.assertTrue('blank' in w[-1].message.args[0])
            
            if lena_available():
                self.assertTrue(image.lena().is_same(pystacia.lena()))
                self.assertTrue('lena' in w[-1].message.args[0])
            
            tmpname = mkstemp()[1] + '.bmp'
            img = sample()
            img.write(tmpname)
            
            self.assertTrue(pystacia.read(tmpname).
                            is_same(image.read(tmpname)))
            self.assertTrue('read' in w[-1].message.args[0])
            
            self.assertTrue(pystacia.read_blob(img.get_blob('bmp')).
                            is_same(image.read_blob(img.get_blob('bmp'))))
            
            self.assertTrue(pystacia.read_raw(**img.get_raw('rgb')).
                            is_same(image.read_raw(**img.get_raw('rgb'))))
            
            img.close()
            
            for symbol in ['magick_logo', 'wizard',
                           'netscape', 'granite', 'rose']:
                self.assertTrue(getattr(image, symbol)().
                                is_same(getattr(pystacia, symbol)()))
                self.assertTrue(symbol in w[-1].message.args[0])
                
            self.assertIsInstance(pystacia.Image(), image.Image)
            
            names = ['composites', 'types', 'filters', 'colorspaces',
                     'compressions', 'axes']
            for name in names:
                self.assertEqual(getattr(pystacia, name).x,
                                  getattr(image, name).x)
                self.assertTrue(name in w[-1].message.args[0])


try:
    from warnings import catch_warnings, simplefilter
except ImportError:
    pass
from tempfile import mkstemp

from pystacia import image
from pystacia.image import colorspaces, types
from pystacia.tests.common import sample
