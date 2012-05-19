# coding: utf-8

# pystacia/tests/color_tests.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from re import match

from pystacia.tests.common import TestCase


class ColorTest(TestCase):
    def test_instantiate(self):
        class Subclass(color.Color):
            pass

        red = color.from_string('red')
        self.assertIsInstance(red, color.Color)

        red = color.from_string('red', factory=Subclass)
        self.assertIsInstance(red, Subclass)

        registry.color_factory = Subclass
        red = color.from_string('red')
        self.assertIsInstance(red, Subclass)

        registry.color_factory = color.Color

    def test_int24(self):
        black = color.from_int24(0)
        self.assertEqual(black, color.from_rgb(0, 0, 0))
        white = color.from_int24(0xffffff)
        self.assertEqual(white, color.from_rgb(1, 1, 1))
        green = color.from_int24(0x00ff00)
        self.assertEqual(green, color.from_rgb(0, 1, 0))

        self.assertEqual(black.get_int24(), 0)
        self.assertEqual(white.get_int24(), 0xffffff)
        self.assertEqual(green.get_int24(), 0xff00)

    def test_cast(self):
        red = color.from_string('red')
        self.assertEqual(id(color.cast(red)), id(red))
        self.assertEqual(color.cast(10), color.from_int24(10))
        self.assertEqual(color.cast('violet'), color.from_string('violet'))
        self.assertEqual(color.cast((0, 1, 0)), color.from_rgb(0, 1, 0))
        self.assertEqual(color.cast((0, 1, 1, 0.5)),
                          color.from_rgba(0, 1, 1, 0.5))
        self.assertRaisesRegexp(PystaciaException, 'Cannot cast',
                                lambda: color.cast((0, 1)))
        self.assertRaisesRegexp(PystaciaException, 'Cannot cast',
                                lambda: color.cast((0, 1, 2, 3, 4)))

    def test_copy(self):
        red = color.from_string('red')
        self.assertEqual(red.copy(), red)
        self.assertNotEqual(id(red), id(red.copy()))

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

    def test_rgb8(self):
        red = color.from_string('red')
        self.assertEqual(red.get_rgb8(), (255, 0, 0))
        green = color.from_string('lime')
        self.assertEqual(green.get_rgb8(), (0, 255, 0))
        blue = color.from_string('blue')
        self.assertEqual(blue.get_rgb8(), (0, 0, 255))

    def test_hsl(self):
        red = color.from_string('red')
        self.assertEqual(red.get_hsl(), (0, 1, 0.5))
        white = color.from_string('white')
        self.assertEqual(white.get_hsl(), (0, 0, 1))
        white = color.from_string('black')
        self.assertEqual(white.get_hsl(), (0, 0, 0))

        self.assertEqual(color.from_hsl(0, 1, 0.5), 'red')
        self.assertEqual(color.from_hsl(0, 0, 1), 'white')
        self.assertEqual(color.from_hsl(0, 0, 0), 'black')

    def test_from_string(self):
        white = color.from_string('white')
        self.assertEqual(white.get_rgba(), (1, 1, 1, 1))
        red = color.from_string('red')
        self.assertEqual(red.get_rgba(), (1, 0, 0, 1))

    def test_saturate(self):
        self.assertEqual(saturate(0.5), 0.5)
        self.assertIsInstance(saturate(0.0), int)
        self.assertEqual(saturate(0.0), 0)
        self.assertIsInstance(saturate(1.0), int)

    def test_repr(self):
        for x in [color.from_string(x) for x in
                  ['red', 'green', 'blue', 'gray']]:
            rgba = x.get_rgba()
            float_re = '(\d(\.\d+)?)'
            regexp = (formattable('<Color\(r={0},g={0},b={0},a={0}\)').
                format(float_re))
            result = match(regexp, repr(x))
            groups = tuple(float(v) for i, v in
                           enumerate(result.groups()) if not i % 2)
            self.assertEqual(groups, rgba)

    def test_factory(self):
        colors = color.Factory()

        self.assertEqual(colors.red, color.from_string('red'))
        self.assertEqual(colors.gray, color.from_string('gray'))

    def test_eq(self):
        red = color.from_string('red')
        self.assertEqual(red, red.copy())
        self.assertEqual(red, 'red')
        self.assertEqual(red, '#f00')
        self.assertEqual(red, 0xff0000)
        self.assertEqual(red, (1, 0, 0))
        self.assertEqual(red, (1, 0, 0, 1))

from pystacia.color._impl import saturate
from pystacia import color, registry
from pystacia.util import PystaciaException
from pystacia.compat import formattable
