# coding: utf-8

# pystacia/image/_impl/blur.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import six

if not six.PY3:
    from future_builtins import zip


def _make_radius_strength_bias(c_name, names, order=None):
    def function(image, *args):
        kwargs = dict(zip(names, args))

        if kwargs['strength'] is None:
            kwargs['strength'] = kwargs['radius']

        if 'bias' in kwargs and kwargs['bias'] is None:
            kwargs['bias'] = 0

        order_ = order or names

        values = [kwargs[k] for k in order_]

        c_call(image, c_name, *values)

    return function


blur = _make_radius_strength_bias('blur', ['radius', 'strength'])


gaussian_blur = _make_radius_strength_bias(
    'gaussian_blur', ['radius', 'strength', 'bias'])


motion_blur = _make_radius_strength_bias(
    'motion_blur', ['radius', 'angle', 'strength', 'bias'],
    ['radius', 'strength', 'angle', 'bias'])


adaptive_blur = _make_radius_strength_bias(
    'adaptive_blur', ['radius', 'strength', 'bias'])


sharpen = _make_radius_strength_bias(
    'sharpen', ['radius', 'strength', 'bias'])


adaptive_sharpen = _make_radius_strength_bias(
    'adaptive_sharpen', ['radius', 'strength', 'bias'])


detect_edges = _make_radius_strength_bias('edge', ['radius', 'strength'])


#TODO: moving center here
def radial_blur(image, angle):
    """Performs radial blur.

       :param angle: Blur angle in degrees
       :type angle: ``float``

       Radial blurs image within given angle.

       This method can be chained.
    """
    c_call(image, 'radial_blur', angle)


def denoise(image):
    """Attempt to remove noise preserving edges.

       Applies a digital filter that improves the quality of a
       noisy image.

       This method can be chained.
    """
    c_call(image, 'enhance')


def despeckle(image):
    """Attempt to remove speckle preserving edges.

       Resulting image almost solid color areas are smoothed preserving
       edges.

       This method can be chained.
    """
    c_call(image, 'despeckle')


emboss = _make_radius_strength_bias('emboss', ['radius', 'strength'])


from pystacia.api.func import c_call
