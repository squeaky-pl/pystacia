# coding: utf-8
# pystacia/tests/lazyenum_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
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
    
    def repr_test(self):
        asd_xyz = cast('asd', 'xyz')
        self.assertEqual(repr(asd_xyz), "pystacia.lazyenum.enum('asd').xyz")


from pystacia.lazyenum import enum, cast
