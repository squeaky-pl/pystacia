# coding: utf-8

# pystacia/image/generic.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


def checkerboard(width, height, factory=None):
    """Returns standard checkerboard image

       :param width: width  in pixels
       :type width: ``int``
       :param height: height in pixels
       :type height: ``int``
       :rtype: :class:`pystacia.image.Image` or factory
    """
    return io.read('pattern:checkerboard', width, height, factory)


def blank(width, height, background=None, factory=None):
    """Create :class:`Image` with monolithic background

       :param width: Width in pixels
       :type width: ``int``
       :param height: Height in pixels
       :type height: ``int``
       :param background: background color, defaults to fully transparent
       :type background: :class:`pystacia.Color`

       Creates blank image of given dimensions filled with background color.

       >>> blank(32, 32, color.from_string('red'))
       <Image(w=32,h=32,16bit,rgb,palette) object at 0x108006000L>
    """
    if not background:
        background = 'transparent'

    return io.read('xc:' + str(background), width, height, factory)


def noise(width, height, grayscale=False, factory=None):
    """Create image filled with monolithic random noise

       :param width: Width in pixels
       :type width: ``int``
       :param height: Height in pixels
       :type height: ``int``
       :param grayscale: Whether noise should be grayscale

       By defult returns an image filled with color noise.
       The image contains grayscale noise if grayscale is set to ``True``.
    """

    image = blank(width, height, 'white')
    image.add_noise(noise_type='random')

    if grayscale:
        image.type = 'grayscale'

    return image


def plasma(width, height, type=None, factory=None):  # @ReservedAssignment
    """Create plasma generic image

        :param width: Width in pixels
        :type width: ``int``
        :param height: Height in pixels
        :type height: ``int``

        :rtype: :class:`pystacia.image.Image`
    """
    spec = 'plasma:'
    if type:
        spec += type

    return io.read(spec, width, height, factory=factory)


from pystacia.image._impl import io
