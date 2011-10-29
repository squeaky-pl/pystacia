# coding: utf-8
# pystacia/tests/lazyenum_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from unittest import TestCase


class Enum(TestCase):
    def test(self):
        composite = enum('composite')
        
        self.assertEquals(composite.name, 'composite')
        self.assertEquals(composite.atop.name, 'atop')
        
        #test memoized
        self.assertEquals(enum('qwerty'), enum('qwerty'))
        
        self.assertEquals(composite.qwerty, composite.qwerty)
        self.assertEquals(id(composite.qwerty), id(composite.qwerty))
        
        self.assertNotEqual(composite.qwerty, composite.abc)


from pystacia.lazyenum import enum
