def sketch(image, radius, angle, strength):
    if strength == None:
        strength = radius
    
    c_call(image, 'sketch', radius, strength, angle)


def oil_paint(image, radius):
    c_call(image, 'oil_paint', radius)


def spread(image, radius):
    c_call(image, 'spread', radius)


def dft(image, magnitude):
    magnitude = bool(magnitude)
    copy = image.copy()
    
    c_call(copy, 'forward_fourier_transorm', magnitude)
    
    first = blank(*image.size)
    second = blank(*image.size)
    
    first.overlay(copy, composite=composites.copy)
    
    c_call(image, 'next')
    
    second.overlay(copy, composite=composites.copy)
    
    copy.close()
    
    return (first, second)


def fx(image, expression):
    resource = c_call(image, 'fx', expression)
    
    image._free()
    image.__init__(resource)


from pystacia.api.func import c_call
from pystacia.image import blank, composites
