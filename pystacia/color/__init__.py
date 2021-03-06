# coding: utf-8

# pystacia/color/__init__.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import division

from six import integer_types, string_types


"""Various color-related functions and objects."""


def _instantiate(factory):
    """Return new color object

       Not to be used directly.
    """
    return registry.get('color_factory', override=factory)()


def from_string(value, factory=None):
    """Create :class:`Color` from string.

       :param value: CSS color specification
       :type value: ``str``
       :param factory: alternative :class:`Color` subclass to use
       :rtype: :class:`Color` or factory instance

       Creates new instance from a valid color specification string
       as in `CSS` 2.1. Supported formats include rgb, rgba, hsl, hsla,
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
    color = _instantiate(factory)
    color.set_string(value)

    return color


def from_rgb(r, g, b, factory=None):
    """Create opaque :class:`Color` from red, green and blue components.

       :param r: red component
       :param g: green component
       :param b: blue component
       :param factory: alternative :class:`Color` subclass to use
       :rtype: :class:`Color` or factory instance

       Red, green and blue components should be numbers between 0 and 1
       inclusive. Resulting color is opaque (alpha channel equal to 1).
       When factory is specified this type is used instead of
       default :class:`Color` type.

       >>> from_rgb(0.5, 1, 0.5)
       <Color(r=0.5,g=1,b=0.5,a=1) object at 0x103266200L>
    """
    color = _instantiate(factory)
    color.set_rgb(r, g, b)

    return color


def from_rgb8(r, g, b, factory=None):
    """Create opaque :class:`Color` from red, green and blue components.

       :param r: red component
       :param g: green component
       :param b: blue component
       :param factory: alternative :class:`Color` subclass to use
       :rtype: :class:`Color` or factory instance

       Red, green and blue components should be integral numbers between 0
       and 255 inclusive. Resulting color is opaque (alpha channel equal to 1).
       When factory is specified this type is used instead of
       default :class:`Color` type.

       >>> from_rgb8(255, 0, 255)
       <Color(r=1,g=0,b=1,a=1) object at 0x103266200L>
    """
    return from_rgb(r / 255, g / 255, b / 255, factory)


def from_rgba(r, g, b, a, factory=None):
    """Create :class:`Color` from red, green, blue and alpha components.

       :param r: red component
       :param g: green component
       :param b: blue component
       :param a: alpha component
       :param factory: alternative :class:`Color` subclass to use
       :rtype: :class:`Color` or factory instance

       Red, green, blue and alpha components should be numbers between 0 and 1
       inclusive.

       >>> from_rgba(1, 1, 0, 0.5)
       <Color(r=1,g=1,b=0,a=0.5) object at 0x103222600L>
    """
    color = from_rgb(r, g, b, factory)
    color.alpha = a

    return color


def from_int24(value, factory=None):
    """Create :class:`Color` from 24 bit integer representation.

       :param value: RGB triplet in 24 bits with high 8 bits being red
       :param factory: alternative :class:`Color` subclass to use
       :rtype: :class:`Color` or factory instance

       Interprets an integer as an 24 bit integer representation of RGB with
       highest 8 bits representing red channel.

       >>> from_int24(0xffffff)
       <Color(r=1,g=1,b=1,a=1) object at 0x103222600L>
    """
    return from_rgb8(value & 0xff0000, value & 0xff00, value & 0xff, factory)


def from_hsl(h, s, l, factory=None):
    color = _instantiate(factory)
    color.set_hsl(h, s, l)
    return color

from pystacia.common import Resource
from pystacia.compat import formattable


def _make_component(name):
    doc = formattable("""Set or get {0} channel information.

       The value ought to be a float between 0 and 1.

       :rtype: ``float`` or ``int``
    """).format(name)

    def fget(self):
        return getattr(impl, 'get_' + name)(self)

    def fset(self, value):
        getattr(impl, 'set_' + name)(self, value)

    return property(fget, fset, doc=doc)


class Color(Resource):

    """Object representing color information."""

    _api_type = 'pixel'

    def _alloc(self):
        return impl.alloc()

    def _free(self):
        impl.free(self)

    def _clone(self):
        return impl.clone(self)

    red = _make_component('red')

    r = red
    """Convenience synonym for :attr:`red`."""

    green = _make_component('green')

    g = green
    """Convenience synonym for :attr:`green`."""

    blue = _make_component('blue')

    b = blue
    """Convenience synonym for :attr:`blue`."""

    alpha = _make_component('alpha')

    a = alpha
    """Convenience synonym for :attr:`alpha`."""

    def get_rgb(self):
        """Return red, green and blue components.

           :rtype: tuple

           Returns tuple containing red, green and blue channel information
           as numbers between 0 and 1.
        """
        return (self.r, self.g, self.b)

    def get_rgb8(self):
        """Return red, gren and blue components as 8bit integers

            :rtype: ``tuple``

            Returns tuple containing red, green and blue in this order
            as 8bit integers randing from 0 to 255
        """
        return tuple(int(255 * x) for x in self.get_rgb())

    def get_hsl(self):
        """Return hue, saturation and lightness components.

           :rtype: tuple
        """
        return impl.get_hsl(self)

    def set_hsl(self, hue, saturation, lightness):
        return impl.set_hsl(self, hue, saturation, lightness)

    def get_int24(self):
        """Return RGB triplet as single 24 bit integer.

           Returns an integer representing this color.
           Highest 8 bit represent red channel information.
        """
        r, g, b = self.get_rgb8()
        return (r << 16) | (g << 8) | b

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

    def set_string(self, value):
        """Resets color value of this instance from string.

           Usage and parameters identical to factory function
           :func:`from_string`.
        """
        impl.set_string(self, value)

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

    def __eq__(self, other):
        return self.get_rgba() == cast(other).get_rgba()

    def __str__(self):
        return self.get_string()

    def __repr__(self):
        template = ('<{class_}(r={0},g={1},b={2},a={3})'
                    ' object at {id}>')
        kw = dict(id=hex(id(self)), class_=self.__class__.__name__)

        return formattable(template).format(*self.get_rgba(), **kw)


from pystacia import registry

registry._install_default('color_factory', Color)  # @UndefinedVariable


class Factory(object):

    """Convenience color factory for SVG names"""

    def __getattr__(self, string):
        return from_string(string)


def cast(value):
    if isinstance(value, Color):
        return value
    elif isinstance(value, integer_types):
        return from_int24(value)
    elif isinstance(value, string_types):
        return from_string(value)
    elif value.__len__:
        if len(value) == 3:
            return from_rgb(*value)
        elif len(value) == 4:
            return from_rgba(*value)

    template = formattable('Cannot cast {0} to Color instance.')
    raise PystaciaException(template.format(value))


from pystacia.color import _impl as impl
from pystacia.util import PystaciaException

__exclusions = [
    'division',
    '_instantiate',
    'Resource',
    'Factory',
    'registry',
    'integer_types',
    'string_types',
    'formattable',
    'impl',
    'PystaciaException',
    '__exclusions'
]

__all__ = list(set(globals().keys()) - set(__exclusions))
