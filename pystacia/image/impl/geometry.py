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


def rotate(image, angle):
    c_call(image, 'rotate', from_string('transparent'), angle)


def flip(image, axis):
    if axis.name == 'x':
        c_call(image, 'flip')
    elif axis.name == 'y':
        c_call(image, 'flop')
    else:
        raise PystaciaException('axis must be X or Y')
    
def transpose(image):
    c_call(image, 'transpose')


def transverse(image):
    c_call(image, 'transverse')

from pystacia.image import filters
from pystacia.util import PystaciaException
from pystacia.api.enum import lookup as enum_lookup
from pystacia.api.func import c_call
from pystacia.color import from_string