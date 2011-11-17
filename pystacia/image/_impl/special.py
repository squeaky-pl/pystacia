def sketch(image, radius, angle, strength):
    if strength == None:
        strength = radius
    
    c_call(image, 'sketch', radius, strength, angle)


def add_noise(image, attenuate, noise_type):
    if not noise_type:
        noise_type = 'gaussian'
        
    noise_type = enum_lookup(noise_type, noises)
    
    c_call(image, 'add_noise', noise_type, attenuate)

def oil_paint(image, radius):
    c_call(image, 'oil_paint', radius)


def charcoal(image, radius, strength, bias):
    if strength == None:
        strength = radius
    if bias == None:
        bias = 0

    c_call(image, 'charcoal', radius, strength, bias)


def spread(image, radius):
    c_call(image, 'spread', radius)


def dft(image, magnitude, factory):
    magnitude = bool(magnitude)
    copy = image.copy()
    
    c_call(copy, 'forward_fourier_transorm', magnitude)
    
    width, height = image.size
    
    first = blank(width, height, factory=factory)
    second = blank(width, height, factory=factory)
    
    first.overlay(copy, composite='copy')
    
    c_call(image, 'next')
    
    second.overlay(copy, composite='copy')
    
    copy.close()
    
    return (first, second)


def fx(image, expression):
    resource = c_call(image, 'fx', expression)
    
    image._free()
    image.__init__(resource)


from pystacia.api.func import c_call
from pystacia.image.generic import blank
from pystacia.image.enum import noises
from pystacia.api.enum import lookup as enum_lookup
