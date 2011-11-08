# coding: utf-8
# pystacia/tests/lazyenum_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.tests import TestCase


class Enum(TestCase):
    def name_test(self):
        composite = enum('composite')
        
        self.assertEquals(composite.name, 'composite')
        self.assertEquals(composite.atop.name, 'atop')
        
    
    def memoize_test(self):
        composite = enum('composite')
        
        self.assertEquals(enum('qwerty'), enum('qwerty'))
        
        self.assertEquals(composite.qwerty, composite.qwerty)
        self.assertEquals(id(composite.qwerty), id(composite.qwerty))
        
        self.assertNotEqual(composite.qwerty, composite.abc)
    
    def cast_test(self):
        xyz = cast('abc', 'xyz')
        
        self.assertEquals(xyz.name, 'xyz')
        self.assertEquals(xyz.enum.name, 'abc')
        self.assertEquals(xyz.enum, enum('abc'))
        self.assertEquals(cast(xyz.enum, 'xyz'), xyz.enum.xyz)
        


from pystacia.lazyenum import enum, cast
