from __future__ import with_statement


from threading import Lock
from pystacia.compat import pypy


if pypy:
    # read lock for PyPy
    __lock = Lock()


def read(spec, width=None, height=None, factory=None):
    image = _instantiate(factory)
    
    if width and height:
        c_call('magick', 'set_size', image, width, height)
    
    if pypy:
        __lock.acquire()
    
    c_call(image, 'read', spec)
    
    if pypy:
        __lock.release()
    
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
    
    c_call(image, ('read', 'blob'), blob, len(blob))
    
    #if format:
    #    guard(resource,
    #              lambda: cdll.MagickSetFormat(resource, old_format))
    
    return image


def read_raw(raw, format, width, height,  # @ReservedAssignment
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


def write(image, filename, format,  # @ReservedAssignment
              compression, quality, flatten, background):
    if not format:
        format = splitext(filename)[1][1:]  # @ReservedAssignment
        
    if flatten == None:
        flatten = format in ('jpg', 'jpeg')
        
    if not background:
        background = 'white'
    
    if flatten:
        background = blank(image.width, image.height, background)
        background.overlay(image)
        image = background
        
    with state(image, format=format, compression_quality=quality):
        c_call(image, 'write', filename)


def get_blob(image, format, compression,  # @ReservedAssignment
             quality):
    with state(image, compression=compression, compression_quality=quality):
        format = format.upper()  # @ReservedAssignment
        old_format = c_call('magick', 'get_format', image)
        c_call('magick', 'set_format', image, format)

        size = c_size_t()
        result = c_call(image, ('get', 'blob'), size)
        blob = string_at(result, size.value)
        
        c_call('magick_', 'relinquish_memory', result)
        
        c_call('magick', 'set_format', image, old_format)
        
        return blob

from os.path import splitext
from ctypes import c_size_t, string_at

from pystacia.common import state
from pystacia.image import _instantiate
from pystacia.image.generic import blank
from pystacia.api.func import c_call
