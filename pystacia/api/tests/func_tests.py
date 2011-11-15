# coding: utf-8
# pystacia/api/tests/func_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.tests.common import TestCase


class FuncTest(TestCase):
    def test_exception(self):
        img = sample()
        
        self.assertRaises(PystaciaException,
                          lambda: simple_call('magick', 'set_format',
                                              img, 'lolz'))
        simple_call('magick', 'set_format', img, 'bmp')
        
        img.close()
        
        self.assertRaises(AttributeError,
                          lambda: get_c_method('magick', 'non_existant'))
        self.assertFalse(get_c_method('magick', 'non_existant', throw=False))

from pystacia.tests.common import sample
from pystacia.api.func import simple_call, get_c_method
from pystacia.util import PystaciaException
