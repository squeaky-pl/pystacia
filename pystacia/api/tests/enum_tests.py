# coding: utf-8
# pystacia/api/tests/enum_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.tests.common import TestCase


class Enum(TestCase):
    def test(self):
        composite = enum('composite')
        
        self.assertEqual(lookup(composite.non_existant, (6, 6), throw=False),
                          None)
        self.assertRaisesRegexp(PystaciaException, 'cannot map mnemonic',
                                lambda: lookup(composite.non_existant, (6, 0)))
        self.assertEqual(lookup(composite.undefined, (6, 6, 2, 10)), 0)
        self.assertEqual(lookup(composite.undefined, (2, 6), throw=False),
                          None)
        self.assertEqual(lookup(composite.undefined, (6, 7, 2, 8)), 0)
        self.assertEqual(lookup(composite.darken_intensity, (6, 7, 2, 1)), 66)


from pystacia.api.enum import lookup
from pystacia.lazyenum import enum
from pystacia.util import PystaciaException
