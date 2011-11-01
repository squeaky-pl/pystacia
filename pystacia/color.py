# coding: utf-8
# pystacia/color.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Various color-related functions and objects."""


def from_string(value, factory=None):
    """Create :class:`Color` from string.
    
       :param value: CSS color specification
       :type value: ``str``
       :param factory: alternative :class:`Color` subclass to use
       :rtype: :class:`Color` or factory instance
       
       Creates new instance from a valid color specification string
       as in CSS 2.1. Supported formats include rgb, rgba, hsl, hsla,
       color identifiers, hexadecimal values, integer and percent values
       where applicable. When factory is specified this type
       is used instead of default :class:`Color` type.
       
       >>> from_string('red')
       <Color(r=1,g=0,b=0,a=1) object at 0x10320e400L>
       >>> from_string('rgb(1,1,0)')
       <Color(r=1,g=1,b=0,a=1) object at 0x103270600L>
       >>> from_string('#fff')
       <Color(r=1,g=1,b=1,a=1) object at 0x103251800L>
       >>> from_string('hsla(50%, 100%, 100%, 0.5)')
       <Color(r=0,g=1,b=1,a=0.5) object at 0x103252a00L>
    """
    #ensure we also get "bytes"
    value = b(value)
    wand = cdll.NewPixelWand()
    guard(wand, lambda: cdll.PixelSetColor(wand, value))
    
    if not factory:
        factory = Color
    
    return factory(wand)


def from_rgb(r, g, b, factory=None):
    """Create opaque :class:`Color` from red, green and blue components.
       
       :param r: red component
       :param g: green component
       :param b: blue component
       :param factory: alternative :class:`Color` subclass to use
       :rtype: :class:`Color` or factory instance
       
       Red, gren and blue components should be numbers between 0 and 1
       inclusive. Resulting color is opaque (alpha channel equal to 1).
       When factory is specified this type is used instead of
       default :class:`Color` type.
       
       >>> from_rgb(0.5, 1, 0.5)
       <Color(r=0.5,g=1,b=0.5,a=1) object at 0x103266200L>
    """
    wand = cdll.NewPixelWand()
    
    cdll.PixelSetRed(wand, r)
    cdll.PixelSetGreen(wand, g)
    cdll.PixelSetBlue(wand, b)
    
    if not factory:
        factory = Color
    
    return factory(wand)


def from_rgba(r, g, b, a, factory=None):
    """Create :class:`Color` from red, green, blue and alpha components.
       
       :param r: red component
       :param g: green component
       :param b: blue component
       :param a: alpha component
       :param factory: alternative :class:`Color` subclass to use
       :rtype: :class:`Color` or factory instance
       
       Red, gren, blue and alpha components should be numbers between 0 and 1
       inclusive.
       
       >>> from_rgba(1, 1, 0, 0.5)
       <Color(r=1,g=1,b=0,a=0.5) object at 0x103222600L>
    """
    color = from_rgb(r, g, b, factory)
    
    color.alpha = a
    
    return color

from pystacia.util import only_live


class Color(object):
    
    """Object representing color information."""
    
    def __init__(self, wand=None):
        """Create :class:`Color` object.
           
           :param wand: ImageMagick resource handle
           :type wand: :class:`pystacia.api.type.PixelWand_p`
           
           Not to be used directly. Use one of color factory functions
           such as :func:`from_rgba` or :func:`from_string` instead.
        """
        self.__wand = wand if wand else cdll.NewPixelWand()
        self.__closed = False
        
        _register_cleanup(self)
    
    def red():  # @NoSelf
        d =\
        """Set or get red channel information.
                  
           The value ought to be a float between 0 and 1.
                  
           :rtype: ``float`` or ``int``
        """
        
        def g(self):
            return saturate(cdll.PixelGetRed(self.__wand))
        
        def s(self, value):
            cdll.PixelSetRed(self.__wand, value)
        
        return dict(fget=g, fset=s, doc=d)
        
    red = property(**red())
    
    r = red
    """Convenience synonym for :attr:`red`."""
    
    def green():  # @NoSelf
        d =\
        """Set or get green channel information.
                  
           The value ought to be a float between 0 and 1.
                  
           :rtype: ``float`` or ``int``
        """
        
        def g(self):
            return saturate(cdll.PixelGetGreen(self.__wand))
        
        def s(self, value):
            cdll.PixelSetGreen(self.__wand, value)
        
        return dict(fget=g, fset=s, doc=d)
    
    green = property(**green())
    
    g = green
    """Convenience synonym for :attr:`green`."""
    
    def blue():  # @NoSelf
        d =\
        """Set or get blue channel information.
                  
           The value ought to be a float between 0 and 1.
                  
           :rtype: ``float`` or ``int``
        """
        
        def g(self):
            return saturate(cdll.PixelGetBlue(self.__wand))
        
        def s(self, value):
            cdll.PixelSetBlue(self.__wand, value)
        
        return dict(fget=g, fset=s, doc=d)
    
    blue = property(**blue())

    b = blue
    """Convenience synonym for :attr:`blue`."""
    
    def alpha():  # @NoSelf
        d =\
        """Set or get alpha channel information.
                  
           The value ought to be a float between 0 and 1.
                  
           :rtype: ``float`` or ``int``
        """
        
        def g(self):
            return saturate(cdll.PixelGetAlpha(self.__wand))
        
        def s(self, value):
            cdll.PixelSetAlpha(self.__wand, value)
        
        return dict(fget=g, fset=s, doc=d)
    
    alpha = property(**alpha())
    
    a = alpha
    """Convenience synonym for :attr:`alpha`."""
    
    def get_rgb(self):
        """Return red, green and blue components.
           
           :rtype: tuple
           
           Returns tuple containing red, green and blue channel information
           as numbers between 0 and 1.
        """
        return (self.r, self.g, self.b)
    
    def get_rgba(self):
        """Return red, green, blue and alpha components.
           
           :rtype: ``tuple``
           
           Returns tuple containing red, green, blue and alpha channel
           information as numbers between 0 and 1.
        """
        return self.get_rgb() + (self.a,)
    
    def set_rgb(self, r, g, b):
        """Set red, green and blue components all at once.
           
           :param r: red component
           :param g: green component
           :param b: blue component
           
           Components should be numbers between 0 and 1. Alpha component
           remains unchanged.
        """
        self.r, self.g, self.b = r, g, b
        
    def set_rgba(self, r, g, b, a):
        """Set red, green, blue and alpha components all at once.
           
           :param r: red component
           :param g: green component
           :param b: blue component
           :param a: alpha component
           
           Components should be numbers between 0 and 1.
        """
        self.set_rgb(r, g, b)
        self.a = a
    
    @only_live
    def close(self):
        """Free associted ImageMagick resources.
           
           Object cant be used after calling this method.
        """
        cdll.DestroyPixelWand(self.__wand)
        self.__closed = True
        
    @property
    def closed(self):
        """Check if object is closed.
        
           :rtype: ``bool``
        """
        return self.__closed
    
    @only_live
    def get_string(self):
        """Return string representation of color.
           
           :rtype: ``str``
           
           Returns standard CSS string representation of color either
           ``rgb(r, g, b)`` or ``rgba(r, g, b, a)`` when color is not
           fully opaque.
        """
        if self.alpha == 1:
            template = formattable('rgb({0}, {1}, {2})')
        else:
            template = formattable('rgba({0}, {1}, {2}, {3})')
        
        rgb = tuple(int(x * 255) for x in self.get_rgb())
        
        return template.format(*(rgb + (self.alpha,)))
    
    @property
    def opaque(self):
        """Check if color is fully opaque.
           
           :rtype: ``bool``
           
           Returns ``True`` if alpha component is exactly equal to 1,
           otherwise ``False``.
           
           >>> from_string('red').opaque
           True
           >>> from_string('transparent').opaque
           False
        """
        return self.alpha == 1
    
    @property
    def transparent(self):
        """Check if color is fully transparent.
           
           :rtype: ``bool``
           
           Returns ``True`` if alpha component is exactly equal to 0,
           otherwise ``False``.
           
           >>> from_string('blue').transparent
           False
           >>> from_string('transparent').transparent
           True
        """
        return self.alpha == 0
     
    @property
    @only_live
    def wand(self):
        """Return underlying ImageMagick resource.
        
           :rtype: ``pystacia.api.type.PixelWand_p``.
           
           This can be useful if you want to perform custom operations
           directly coping with ctypes.
        """
        return self.__wand
    
    @only_live
    def copy(self):
        """Return an independent new :class:`Color` object with copied state.
        
        >>> copy = red.copy()
        >>> copy == red
        True
        """
        wand = cdll.ClonePixelWand(self.__wand)
        return Color(wand)
    
    def __eq__(self, other):
        return self.get_rgba() == other.get_rgba()
    
    def __str__(self):
        return self.get_string()
    
    @only_live
    def __repr__(self):
        template = ('<{class_}(r={0},g={1},b={2},a={3})'
                    ' object at {addr}>')
        kw = dict(addr=hex(addressof(self.__wand[0])),
                  class_=self.__class__.__name__)
        
        return formattable(template).format(*self.get_rgba(), **kw)


def saturate(v):
    if v == 0:
        return 0
    elif v == 1:
        return 1
    else:
        return round(v, 4)


from ctypes import addressof

from six import b

from pystacia import cdll, _register_cleanup
from pystacia.api.func import guard
from pystacia.compat import formattable

transparent = from_string('transparent')
