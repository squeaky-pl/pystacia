# coding: utf-8

# pystacia/image/_impl/blur.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


def blur(image, radius, strength):
    if strength is None:
        strength = radius

    c_call(image, 'blur', radius, strength)


def _make_radius_strength_bias(c_name, names, order=None):
    def function(image, *args):
        kwargs = dict(zip(names, args))

        if kwargs['strength'] is None:
            kwargs['strength'] = kwargs['radius']

        if kwargs['bias'] is None:
            kwargs['bias'] = 0

        order_ = order or names

        values = [kwargs[k] for k in order_]

        c_call(image, c_name, *values)

    return function


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


def detect_edges(image, radius, strength):
    if strength is None:
        strength = radius

    c_call(image, 'edge', radius, strength)


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


def emboss(image, radius, strength):
    """Apply edge detecting algorithm.

       :param radius: filter radius
       :type radius: ``int``
       :param stregth: filter strength (sigma)
       :type strength: ``int``

       On a typical photo creates effect of raised edges.

       This method can be chained.
    """
    if strength is None:
        strength = radius

    c_call(image, 'emboss', radius, strength)


from pystacia.api.func import c_call
