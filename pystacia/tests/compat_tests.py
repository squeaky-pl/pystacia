# coding: utf-8
# pystacia/tests/compat_tests.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from sys import version_info

from pystacia.tests.common import TestCase


class Compat(TestCase):
    def test(self):
        if version_info < (2, 6):
            from stringformat import FormattableString
            self.assertEqual(formattable, FormattableString)
        else:
            self.assertEqual(formattable, str)

        if version_info < (3,):
            value = 'abc'
        else:
            value = 'abc'.encode('utf-8')

        self.assertIsInstance(native_str(value), str)
        self.assertEqual(native_str(value), 'abc')

        if version_info >= (3, 2) or (2, 7) <= version_info < (2, 8):
            from ctypes import c_ssize_t as c_ssize_t_
            self.assertEqual(c_ssize_t, c_ssize_t_)

        if version_info < (2, 7):
            from unittest2 import TestCase as TestCase_
            self.assertEqual(TestCase, TestCase_)
        else:
            from unittest import TestCase as TestCase_py
            self.assertEqual(TestCase, TestCase_py)

from pystacia.compat import formattable, native_str, c_ssize_t
