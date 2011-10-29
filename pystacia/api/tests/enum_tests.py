# coding: utf-8
# pystacia/api/tests/enum_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from unittest import TestCase


class Enum(TestCase):
    def test(self):
        composite = enum('composite')
        
        self.assertEquals(lookup(composite.non_existant, (6, 6)), None)
        self.assertEquals(lookup(composite.undefined, (6, 6, 2, 10)), 0)
        self.assertEquals(lookup(composite.undefined, (2, 6, 2, 10)), None)
        self.assertEquals(lookup(composite.undefined, (6, 7, 2, 8)), 0)
        self.assertEquals(lookup(composite.darken_intensity, (6, 7, 2, 1)), 66)


from pystacia.api.enum import lookup
from pystacia.lazyenum import enum
