# coding: utf-8
# pystacia/tests/color_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.tests.common import TestCase


class ColorTest(TestCase):
    def test_int24(self):
        black = color.from_int24(0)
        self.assertEqual(black, color.from_rgb(0, 0, 0))
        white = color.from_int24(0xffffff)
        self.assertEqual(white, color.from_rgb(1, 1, 1))
        green = color.from_int24(0x00ff00)
        self.assertEqual(green, color.from_rgb(0, 1, 0))
        
    def test_cast(self):
        self.assertEqual(color.cast(10), color.from_int24(10))
        self.assertEqual(color.cast('violet'), color.from_string('violet'))
        self.assertEqual(color.cast((0, 1, 0)), color.from_rgb(0, 1, 0))
        self.assertEqual(color.cast((0, 1, 1, 0.5)),
                          color.from_rgba(0, 1, 1, 0.5))
        self.assertRaisesRegexp(PystaciaException, 'Cannot cast',
                                lambda: color.cast((0, 1)))
        self.assertRaisesRegexp(PystaciaException, 'Cannot cast',
                                lambda: color.cast((0, 1, 2, 3, 4)))
    
    def test_get_string(self):
        blue = color.from_string('blue')
        self.assertEqual(blue.get_string(), 'rgb(0, 0, 255)')
        blue.alpha = 0
        self.assertEqual(blue.get_string(), 'rgba(0, 0, 255, 0)')
    
    def test_rgb(self):
        rgb = (1, 0, 0)
        red = color.from_rgb(*rgb)
        
        self.assertEqual((red.red, red.r), (1, 1))
        self.assertEqual((red.green, red.g), (0, 0))
        self.assertEqual((red.blue, red.b), (0, 0))
        self.assertEqual((red.alpha, red.a), (1, 1))
        
        self.assertEqual(red.get_rgb(), rgb)
        self.assertEqual(red.get_rgba(), rgb + (1,))
        
        red.g = 1
        self.assertEqual(red.g, 1)
        self.assertEqual(red.green, 1)
        
        red.set_rgba(0, 1, 1, 0)
        
        self.assertEqual(red.get_rgba(), (0, 1, 1, 0))
    
    def test_hsl(self):
        red = color.from_string('red')
        self.assertEqual(red.get_hsl(), (0, 1, 0.5))
        white = color.from_string('white')
        self.assertEqual(white.get_hsl(), (0, 0, 1))
        white = color.from_string('black')
        self.assertEqual(white.get_hsl(), (0, 0, 0))
    
    def test_from_string(self):
        white = color.from_string('white')
        self.assertEqual(white.get_rgba(), (1, 1, 1, 1))
        red = color.from_string('red')
        self.assertEqual(red.get_rgba(), (1, 0, 0, 1))
    
    def test_saturate(self):
        self.assertEqual(color.saturate(0.5), 0.5)
        self.assertIsInstance(color.saturate(0.0), int)
        self.assertEqual(color.saturate(0.0), 0)
        self.assertIsInstance(color.saturate(1.0), int)
    
    def test_factory(self):
        colors = color.Factory()
        
        self.assertEqual(colors.red, color.from_string('red'))
        self.assertEqual(colors.gray, color.from_string('gray'))


from pystacia import color
from pystacia.util import PystaciaException
