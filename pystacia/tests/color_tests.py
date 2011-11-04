# coding: utf-8
# pystacia/tests/color_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.compat import TestCase


class ColorTest(TestCase):
    def test_int24(self):
        black = color.from_int24(0)
        self.assertEquals(black, color.from_rgb(0, 0, 0))
        white = color.from_int24(0xffffff)
        self.assertEquals(white, color.from_rgb(1, 1, 1))
        green = color.from_int24(0x00ff00)
        self.assertEquals(green, color.from_rgb(0, 1, 0))
        
    def test_cast(self):
        self.assertEquals(color.cast(10), color.from_int24(10))
        self.assertEquals(color.cast('violet'), color.from_string('violet'))
        self.assertEquals(color.cast((0, 1, 0)), color.from_rgb(0, 1, 0))
        self.assertEquals(color.cast((0, 1, 1, 0.5)),
                          color.from_rgba(0, 1, 1, 0.5))
        self.assertRaisesRegexp(PystaciaException, 'Cannot cast',
                                lambda: color.cast((0, 1)))
        self.assertRaisesRegexp(PystaciaException, 'Cannot cast',
                                lambda: color.cast((0, 1, 2, 3, 4)))


class GetStringTest(TestCase):
    def test(self):
        blue = color.from_string('blue')
        self.assertEquals(blue.get_string(), 'rgb(0, 0, 255)')
        blue.alpha = 0
        self.assertEquals(blue.get_string(), 'rgba(0, 0, 255, 0)')


class Copy(TestCase):
    def test(self):
        blue = color.from_string('white')
        blue_copy = blue.copy()
        
        self.assertNotEqual(blue.resource, blue_copy.resource)
        self.assertEquals(blue, blue_copy)


class RgbColor(TestCase):
    def test(self):
        rgb = (1, 0, 0)
        red = color.from_rgb(*rgb)
        
        self.assertEquals((red.red, red.r), (1, 1))
        self.assertEquals((red.green, red.g), (0, 0))
        self.assertEquals((red.blue, red.b), (0, 0))
        self.assertEquals((red.alpha, red.a), (1, 1))
        
        self.assertEquals(red.get_rgb(), rgb)
        self.assertEquals(red.get_rgba(), rgb + (1,))
        
        red.g = 1
        self.assertEquals(red.g, 1)
        self.assertEquals(red.green, 1)
        
        red.set_rgba(0, 1, 1, 0)
        
        self.assertEquals(red.get_rgba(), (0, 1, 1, 0))


class String(TestCase):
    def test(self):
        white = color.from_string('white')
        self.assertEquals(white.get_rgba(), (1, 1, 1, 1))
        red = color.from_string('red')
        self.assertEquals(red.get_rgba(), (1, 0, 0, 1))


class SaturateTest(TestCase):
    def test(self):
        self.assertEquals(color.saturate(0.5), 0.5)
        self.assertIsInstance(color.saturate(0.0), int)
        self.assertEquals(color.saturate(0.0), 0)
        self.assertIsInstance(color.saturate(1.0), int)
        
class FactoryTest(TestCase):
    def test(self):
        colors = color.Factory()
        
        self.assertEquals(colors.red, color.from_string('red'))
        self.assertEquals(colors.gray, color.from_string('gray'))


from pystacia import color
from pystacia.util import PystaciaException
