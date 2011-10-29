# coding: utf-8
# pystacia/tests/magick_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.compat import TestCase


class Magick(TestCase):
    def test_options(self):
        self.assertIsInstance(get_options(), dict)
        
    def test_version(self):
        self.assertIsInstance(get_version(), (tuple, type(None)))


from pystacia.magick import get_options, get_version
