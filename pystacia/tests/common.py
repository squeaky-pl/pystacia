# coding: utf-8

# pystacia/tests/common.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

try:
    from unittest import skip, skipIf, expectedFailure
except ImportError:
    from unittest2 import skip, skipIf, expectedFailure  # NOQA

from unittest import TestCase
if not hasattr(TestCase, 'assertSequenceEqual'):
    from unittest2 import TestCase  # @UnusedImport @UnresolvedImport @Reimport

# python 3.1 misses this one method, copy implementation from Python source
if not hasattr(TestCase, 'assertIsInstance'):
    _MAX_LENGTH = 80

    def safe_repr(obj, short=False):
        try:
            result = repr(obj)
        except Exception:
            result = object.__repr__(obj)
        if not short or len(result) < _MAX_LENGTH:
            return result
        return result[:_MAX_LENGTH] + ' [truncated]...'

    def assertIsInstance(self, obj, cls, msg=None):
        """Same as self.assertTrue(isinstance(obj, cls)), with a nicer
        default message."""
        if not isinstance(obj, cls):
            standardMsg = '%s is not an instance of %r' % (safe_repr(obj), cls)
            self.fail(self._formatMessage(msg, standardMsg))

    TestCase.assertIsInstance = assertIsInstance

from pystacia import image
from pystacia.image import types
from pystacia.image.sample import lena_available


if lena_available():
    sample = image.lena
    sample.size = (512, 512)
    sample.type = types.truecolor
else:
    sample = image.magick_logo
    sample.size = (640, 480)
    sample.type = types.palette
