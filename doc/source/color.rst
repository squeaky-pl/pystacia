==================
Working with color
==================

Couple of methods in Pystacia use color as argument. There are many ways to
factory a color in Pystacia. All the machinery is defined in :mod:`pystcia.color`
As a convention all the channel information for red, blue, green, alpha and so on
is specified as ``float`` numbers between `0` and `1`. It can be misleading
for people used to thinking in 8-bit 0-255 mode. Pystacia uses ``float`` because
of internal 16-bit precision that :term:`ImageMagick` works in and also its `C`
interface uses `float`.

You normally don't instantiate :class:`pystacia.color.Color` directly.
You should rely on factory methods presented below instead.

Creating colors from string
===========================

:func:`pystacia.color.from_string` can be used to synthesize colors from their
string representations. It accepts broad variety of input formats as defined in
:term:`CSS3` `color module <http://www.w3.org/TR/css3-color/>`_.

Well known colors:

>>> color.from_string('transparent')
<Color(r=0,g=0,b=0,a=0) object at 0x10a858c00L>
>>> color.from_string('red')
<Color(r=1,g=0,b=0,a=1) object at 0x103716c00L>
>>> color.from_string('teal')
<Color(r=0,g=0.502,b=0.502,a=1) object at 0x10a856a00L>

Function syntax:

>>> color.from_string('rgb(255, 255, 255)')  # rgb
<Color(r=1,g=1,b=1,a=1) object at 0x108047e00L>
>>> color.from_string('rgb(100%,100%,50%)')  # rgb with percentage
<Color(r=1,g=1,b=0.5,a=1) object at 0x10a817e00L>
>>> color.from_string('rgba(255, 255, 255, 0.5)')  # rgba
<Color(r=1,g=1,b=1,a=0.5) object at 0x10a819a00L>
>>> color.from_string('hsl(120, 100%, 75%)')  # hsl
<Color(r=0.9,g=1,b=0.5,a=1) object at 0x10804a400L>
>>> color.from_string('hsla(240, 100%, 50%, 0.5)')  # hsla
<Color(r=0,g=1,b=0.4,a=0.5) object at 0x1080a0c00L>

Creating colors from floats
===========================

It's not always convenient to use string syntax. You can use
:func:`pystacia.color.from_rgb` and :func:`pystacia.color.from_rgba` to create
colors from numerical values.

>>> color.from_rgb(0, 1, 1)
<Color(r=0,g=1,b=1,a=1) object at 0x1037a2800L>
>>>> color.from_rgba(0.5, 0.5, 0.5, 0.5)
<Color(r=0.5,g=0.5,b=0.5,a=0.5) object at 0x10b058a00L>

You can also create colors by probing them from images with
:meth:`pystacia.image.Image.get_pixel`.

Color class
===========

Once instantiated a :class:`pystacia.color.Color` instance can be queried and
modified.

Channel information
-------------------

Red, blue, green and alpha information can be accessed and modified with
:attr:`pystacia.color.Color.red`, :attr:`pystacia.color.Color.green`,
:attr:`pystacia.color.Color.blue`, :attr:`pystacia.color.Color.alpha`
properties that also have convenience one letter abbreviations:
:attr:`pystacia.color.Color.r`, :attr:`pystacia.color.Color.g`,
:attr:`pystacia.color.Color.b`, :attr:`pystacia.color.Color.a`.

>>> red = color.from_string('red')
>>> red.red
1
>>> red.red == red.r
True
>>> red.green
0
>>> red.green = 1
>>> red.g
1
>>> red.a = 0.5
>>> red
<Color(r=1,g=1,b=0,a=0.5) object at 0x108036200L>

You can also set several channels at once with :meth:`pystacia.color.Color.set_rgb`
and :meth:`pystacia.color.Color.set_rgba` methods:

>>> red.set_rgb(0, 0.5, 1)
>>> red
<Color(r=0,g=0.5,b=1,a=0.5) object at 0x108036200L>
>>> red.set_rgba(1, 1, 1, 0.1)
>>> red
<Color(r=1,g=1,b=1,a=0.1) object at 0x108036200L>

Also access all channels at once as tuples with  :meth:`pystacia.color.Color.get_rgb`
and :meth:`pystacia.color.Color.get_rgba`:

>>> red.get_rgb()
(1, 1, 1)
>>> red.get_rgba()
(1, 1, 1, 0.1)

To return value :term:`CSS3` string representation of color use :meth:`pystacia.color.Color.get_string`
or cast instance with :func:`str`:

>>> red.get_string()
'rgba(255, 255, 255, 0.1)'
>>> str(red)
'rgba(255, 255, 255, 0.1)'

Testing for transparency
------------------------

You can query if color is fully transparent with :attr:`pystacia.color.Color.transparent`
property whilst you can use :attr:`pystacia.color.Color.opaque` to test if color
is fully opaque.

>>> red = color.from_string('red')
>>> red.opaque
True
>>> red.transparent
False
>>> transparent = color.from_string('transparent')
>>> transparent.opaque
False
>>> transparent.transparent
True
