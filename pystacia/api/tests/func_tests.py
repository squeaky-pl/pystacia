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

from pystacia.tests import sample
from pystacia.api.func import simple_call
from pystacia.util import PystaciaException
