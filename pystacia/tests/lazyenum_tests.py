# coding: utf-8
# pystacia/tests/lazyenum_tests.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.tests.common import TestCase


class Enum(TestCase):
    def name_test(self):
        composite = enum('composite')
        
        self.assertEqual(composite.name, 'composite')
        self.assertEqual(composite.atop.name, 'atop')
    
    def memoize_test(self):
        composite = enum('composite')
        
        self.assertEqual(enum('qwerty'), enum('qwerty'))
        
        self.assertEqual(composite.qwerty, composite.qwerty)
        self.assertEqual(id(composite.qwerty), id(composite.qwerty))
        
        self.assertNotEqual(composite.qwerty, composite.abc)
    
    def cast_test(self):
        xyz = cast('abc', 'xyz')
        
        self.assertEqual(xyz.name, 'xyz')
        self.assertEqual(xyz.enum.name, 'abc')
        self.assertEqual(xyz.enum, enum('abc'))
        self.assertEqual(cast(xyz.enum, 'xyz'), xyz.enum.xyz)
        
        self.assertRaisesRegexp(PystaciaException, 'Cannot cast',
                                lambda: cast(2, 'asd'))
        self.assertRaisesRegexp(PystaciaException, 'Attempted to cast',
                                lambda: cast(xyz.enum, cast('fgh', 'rty')))
        self.assertEqual(id(xyz), id(cast(xyz.enum, xyz)))
        self.assertRaisesRegexp(PystaciaException, 'Cannot cast',
                                lambda: cast('asd', 2))
        self.assertRaisesRegexp(PystaciaException, 'Cannot cast',
                                lambda: xyz.enum.cast(1))
    
    def eq_test(self):
        circle = cast('shape', 'circle')
        square = cast('shape', 'square')
        
        self.assertEquals(circle, 'circle')
        self.assertNotEqual(circle, 'square')
        self.assertEqual(square, 'square')
        self.assertNotEqual(circle, 3)
        
    def str_test(self):
        circle = cast('shape', 'circle')
        square = cast('shape', 'square')
        
        self.assertEqual(str(circle), 'circle')
        self.assertEqual(str(circle.enum), 'shape')
        self.assertEqual(str(square), 'square')
    
    def repr_test(self):
        asd_xyz = cast('asd', 'xyz')
        self.assertEqual(repr(asd_xyz), "pystacia.lazyenum.enum('asd').xyz")


from pystacia.lazyenum import enum, cast
from pystacia.util import PystaciaException
