# coding: utf-8

# pystacia/tests/common.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import with_statement

from threading import Lock
from functools import partial
import weakref
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


__sample = None
__lock = Lock()


def __weakrefed(factory):
    """Perform weakref memoization of factory call value."""
    global __sample

    if not __sample:
        with __lock:
            sample = factory()
            if not __sample:
                __sample = weakref.ref(sample)
    else:
        sample = __sample()
        if not sample:
            with __lock:
                if not sample:
                    sample = factory()
                    __sample = weakref.ref(sample)

    return sample.copy()


if lena_available():
    sample = partial(__weakrefed, image.lena)
    sample_size = (512, 512)
    sample_type = types.truecolor
else:
    sample = partial(__weakrefed, image.magick_logo)
    sample_size = (640, 480)
    sample_type = types.palette
