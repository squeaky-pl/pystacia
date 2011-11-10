from __future__ import with_statement


def read(spec, width=None, height=None, factory=None):
    """Read special :term:`ImageMagick` image resource"""
    if not factory:
        factory = Image
        
    image = factory()
    
    if width and height:
        c_call('magick', 'set_size', image, width, height)
    
    c_call(image, 'read', spec)
    
    return image

def read_blob(blob, format=None, factory=None):  # @ReservedAssignment
    if not factory:
        factory = Image
    
    image = factory()
    
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
    if not factory:
        factory = Image
    
    image = factory()
    
    c_call('magick', 'set_size', image, width, height)
    c_call('magick', 'set_depth', image, depth)
    format = format.upper()  # @ReservedAssignment
    c_call('magick', 'set_format', image, format)
        
    c_call(image, ('read', 'blob'), raw, len(raw))
    
    return image


def write(image, filename, format=None,  # @ReservedAssignment
              compression=None, quality=None):
    with state(image, format=format, compression_quality=quality):
#    if format:
#        format = b(format.upper())  # @ReservedAssignment
#        old_format = cdll.MagickGetImageFormat(resource)
#        template = formattable('Format "{0}" unsupported')
#        guard(resource,
#              lambda: cdll.MagickSetImageFormat(resource, format),
#              template.format(format))
#        
#    if quality != None:
#        old_quality = cdll.MagickGetImageCompressionQuality(resource)
#        guard(resource,
#              lambda: cdll.MagickSetImageCompressionQuality(resource,
#                                                            quality))
        c_call(image, 'write', filename)
#    if quality != None:
#        guard(resource,
#              lambda: cdll.MagickSetImageCompressionQuality(resource,
#                                                            old_quality))
#    if format:
#        guard(resource,
#              lambda: cdll.MagickSetImageFormat(resource, old_format))

def get_blob(image, format, compression=None,  # @ReservedAssignment
             quality=None):
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
        

from ctypes import c_size_t, string_at

from pystacia.common import state
from pystacia.image import Image
from pystacia.api.func import c_call