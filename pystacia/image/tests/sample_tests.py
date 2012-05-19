# coding: utf-8

# pystacia/iamge/tests/sample_tests.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.tests.common import TestCase
from pystacia.image import types


data = {
    'lena': {
        'size': (512, 512),
        'depth': 8,
        'type': types.truecolor,
    },
    'magick_logo': {
        'size': (640, 480),
        'depth': 8,
        'type': types.palette,
    },
    'netscape': {
        'size': (216, 144),
        'depth': 8,
        'type': types.palette,
    },
    'rose': {
        'size': (70, 46),
        'depth': 8,
        'type': types.truecolor,
    },
    'wizard': {
        'size': (480, 640),
        'depth': 8,
        'type': types.palette,
    }
}


class SampleTest(TestCase):
    def test(self):
        if not lena_available():
            del data['lena']

        for sample, params in data.items():
            img = getattr(image, sample)()

            for param, value in params.items():
                self.assertEqual(getattr(img, param), value)

            img.close()


from pystacia import image
from pystacia.image.sample import lena_available
