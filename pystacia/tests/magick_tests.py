# coding: utf-8

# pystacia/tests/magick_tests.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from six import string_types

from pystacia.tests.common import TestCase


class MagickTest(TestCase):
    def test_options(self):
        self.assertIsInstance(get_options(), dict)

    def test_version(self):
        self.assertIsInstance(get_version(), (tuple, type(None)))
        self.assertIsInstance(get_version_str(), string_types)

    def test_formats(self):
        formats = get_formats()
        self.assertIn('bmp', formats)


from pystacia.magick import (get_options, get_version, get_version_str,
                            get_formats)
