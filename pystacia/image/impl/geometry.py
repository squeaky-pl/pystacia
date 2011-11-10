def rescale(image, width, height, factor, filter, blur):  # @ReservedAssignment
    if not filter:
        filter = filters.undefined  # @ReservedAssignment
    
    if not width and not height:
        if not factor:
            msg = 'Either width, height or factor must be provided'
            raise PystaciaException(msg)
        
        width, height = image.size
        if not hasattr(factor, '__getitem__'):
            factor = (factor, factor)
        width, height = int(width * factor[0]), int(height * factor[1])
    
    c_call(image, 'resize', width, height, enum_lookup(filter), blur)

def resize(image, width, height, x, y):
    c_call(image, 'crop', width, height, x, y)

from pystacia.image import filters
from pystacia.util import PystaciaException
from pystacia.api.enum import lookup as enum_lookup
from pystacia.api.func import c_call