# coding: utf-8
# pystacia/tests/compat_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.compat import TestCase


class Compat(TestCase):
    def test(self):
        if version_info < (2, 6):
            from stringformat import FormattableString
            self.assertEquals(formattable, FormattableString)
        else:
            self.assertEquals(formattable, str)
            
        if version_info < (3,):
            value = 'abc'
        else:
            value = 'abc'.encode('utf-8')
            
        self.assertIsInstance(native_str(value), str)
        self.assertEquals(native_str(value), 'abc')
        
        if version_info >= (2, 7):
            from ctypes import c_ssize_t as c_ssize_t_
            self.assertEquals(c_ssize_t, c_ssize_t_)
            
        if version_info < (2, 7):
            from unittest2 import TestCase as TestCase_
            self.assertEquals(TestCase, TestCase_)
        else:
            from unittest import TestCase as TestCase_py
            self.assertEquals(TestCase, TestCase_py)


from sys import version_info
from pystacia.compat import formattable, native_str, c_ssize_t
