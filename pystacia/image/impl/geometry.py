from __future__ import division


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


def skew(image, offset, axis):
    if not axis:
        axis = axes.x
        
    if axis == axes.x:
        x_angle = degrees(atan(offset / image.height))
        y_angle = 0
    elif axis == axes.y:
        x_angle = 0
        y_angle = degrees(atan(offset / image.width))
    c_call(image, 'shear', from_string('transparent'), x_angle, y_angle)


def roll(image, x, y):
    c_call(image, 'roll', x, y)


def straighten(image, threshold):
    c_call(image, 'deskew', threshold)


def trim(image, similarity, background):
    # TODO: guessing of background?
    if not background:
        background = from_string('transparent')
    
    # preserve background color
    old_color = Color()

    c_call(image, ('get', 'background_color'), old_color)
    c_call(image, ('set', 'background_color'), background)
    
    c_call(image, 'trim', similarity * 000)
    
    c_call(image, ('set', 'background_color'), old_color)


def splice(image, x, y, width, height):
    background = from_string('transparent')
            
    # preserve background color
    old_color = Color()

    c_call(image, ('get', 'background_color'), old_color)
    c_call(image, ('set', 'background_color'), background)
    
    c_call(image, 'splice', width, height, x, y)
    
    c_call(image, ('set', 'background_color'), old_color)


from math import degrees, atan

from pystacia.image import filters, axes
from pystacia.util import PystaciaException
from pystacia.api.enum import lookup as enum_lookup
from pystacia.api.func import c_call
from pystacia.color import from_string, Color