from __future__ import with_statement


def read_special(spec, width=None, height=None, factory=None):
    """Read special :term:`ImageMagick` image resource"""
    if not factory:
        factory = Image
        
    image = factory()
    
    if width and height:
        c_call('magick', 'set_size', image, width, height)
    
    c_call(image, 'read', spec)
    
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

from pystacia.common import state
from pystacia.image import Image
from pystacia.api.func import c_call