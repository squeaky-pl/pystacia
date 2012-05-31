# coding: utf-8

# pystacia/image/_impl/io.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import with_statement

from os.path import splitext


def read(spec, width=None, height=None, factory=None):
    image = _instantiate(factory)

    if width and height:
        c_call('magick', 'set_size', image, width, height)

    c_call(image, 'read', spec)

    return image


def read_blob(blob, format, factory):  # @ReservedAssignment
    image = _instantiate(factory)

    #resource = image.resource
    #if format:
        # ensure we always get bytes
    #    format = b(format.upper())  # @ReservedAssignment
    #    old_format = cdll.MagickGetImageFormat(resource)
    #    template = formattable('Format "{0}" unsupported')
    #    guard(resource,
    #          lambda: cdll.MagickSetFormat(resource, format),
    #          template.format(format))

    if hasattr(blob, 'read'):
        blob = blob.read()

    c_call(image, ('read', 'blob'), blob, len(blob))

    #if format:
    #    guard(resource,
    #              lambda: cdll.MagickSetFormat(resource, old_format))

    return image


def read_raw(raw, format, width, height, # @ReservedAssignment
             depth, factory=None):
    image = _instantiate(factory)

    c_call('magick', 'set_size', image, width, height)
    c_call('magick', 'set_depth', image, depth)
    format = format.upper()  # @ReservedAssignment
    c_call('magick', 'set_format', image, format)

    if hasattr(raw, 'read'):
        raw = raw.read()

    c_call(image, ('read', 'blob'), raw, len(raw))

    return image


def write(image, filename, format, # @ReservedAssignment
              compression, quality, flatten, background):
    if not format:
        format = splitext(filename)[1][1:].lower()  # @ReservedAssignment

    if flatten == None:
        flatten = (image.type.name.endswith('matte') and
                   format not in ('png', 'tiff', 'tif', 'bmp', 'gif'))

    if not background:
        background = 'white'

    if flatten:
        background = blank(image.width, image.height, background)
        background.overlay(image)
        image = background

    with state(image, format=format, compression_quality=quality):
        c_call(image, 'write', filename)


def get_blob(image, format, compression, # @ReservedAssignment
             quality):
    with state(image, compression=compression, compression_quality=quality):
        format = format.upper()  # @ReservedAssignment
        old_format = c_call('magick', 'get_format', image)
        c_call('magick', 'set_format', image, format)

        size = c_size_t()
        result = c_call(image, ('get', 'blob'), byref(size))

        #from nose.tools import set_trace; set_trace()

        blob = string_at(result, size.value)

        c_call('magick_', 'relinquish_memory', result)

        c_call('magick', 'set_format', image, old_format)

        return blob


def ping(filename):
    image = _instantiate(None)

    c_call(image, 'ping', filename)

    result = {
        'width': image.width,
        'height': image.height,
        'format': image.format
    }

    image.close()
    return result


def ping_blob(blob):
    image = _instantiate(None)

    if hasattr(blob, 'read'):
        blob = blob.read()

    c_call(image, ('ping', 'blob'), blob, len(blob))

    result = {
        'width': image.width,
        'height': image.height,
        'format': image.format
    }

    image.close()
    return result


from pystacia.common import state
from pystacia.image import _instantiate
from pystacia.image.generic import blank
from pystacia.api.func import c_call
from pystacia.api.compat import c_size_t, string_at, byref

