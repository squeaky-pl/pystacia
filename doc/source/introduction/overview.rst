========
Overview
========

The philiosophy
===============

Modules
-------

Pacakge :mod:`tinyimg` is divided into several submodules of which
:mod:`tinyimg.image` and :mod:`tinyimg.color` are of most interest
to readers. For convenience reasons symbols from `tinyimg.image` are
imported directly into :mod:`tinyimg` and :mod:`tinyimg.color` is
accessible as :attr:`tinyimg.color` attribute under :mod:`tinyimg`.

For quick experiments in a console you can perform `from tinyimg import *`. 
Several attributes got pulled into your namespace including:

- :func:`tinyimg.image.read`, :func:`tinyimg.image.read_blob` and
  :func:`tinyimg.image.read_raw` image factories
- :attr:`tinyimg.image.composite`, :attr:`tinyimg.image.types`,
  :attr:`tinyimg.image.filters`, :attr:`tinyimg.image.colorspaces`,
  :attr:`tinyimg.image.axes` lazy enumerations
- :func:`tinyimg.lena` and :func:`tinyimg.magick_logo` sample image factories


Classes and factories
---------------------

tinyimg is an object oriented imaging library. It uses factory functions to
create objects representing concepts like :class:`tinyimg.image.Image` or
:class:`tinyimg.color.Color`. You don't typically use class constructors to
create objects and generally you shouldn't unless you really know what you
are doing. You should rely on factories instead.
::
    
    """Create an image object from read factory"""
    
    from tinyimg import read
    image = read('example.jpg')
    
    
    """Create a color object from from_string factory"""
    
    from tinyimg import color
    red = color.from_string('red')

Constants
---------

Many tinyimg methods take :term:`C` enum-like mnemonics. For example to specify
which axis to perform transformation along you can use :attr:`axes.x`. These
names are symbolic representation of underlying `C` constants. They are
lazily resolved during runtime to their integral value.
::

    """Skew an image by 5 pixels along Y axis"""
    
    image.skew(5, axes.y)
    
There are several lazy enums defined. Most of them inside :mod:`tinyimg.image`
but they are also for you convenience imported into main :mod:`tinyimg` module.
Some of them are listed below:

- :attr:`tinyimg.image.types`: image types such as :attr:`types.bilevel` for
  monochrome image, `types.pallette`, `types.grayscale` and `types.truecolor`
- :attr:`tinyimg.image.colorspace`: color-spaces such as :attr:`colorspaces.rgb`
  or `colorspaces.ycbcr`.
- :attr:`tinyimg.image.filters`: sampling filters used typically in rescaling
  algorithms including popular :attr:`filters.point`, :attr:`filters.bilinear`
  or :attr:`filters.sinc` typically used in :meth:`tinyimg.image.Image.rescale`.
- :attr:`tinyimg.image.composites`: :attr:`composite.over` or :attr:`composite.hue`
  used with :meth:`tinyimg.image.Image.overlay`.
- :attr:`tinyimg.image.axes`: :attr:`axes.x` and :attr:`axes.y` axes

Method chaining
---------------

By default methods of :class:`tinyimg.image.Image` are chainable i.e. you
can construct code using long string of methods forming a chain such as::

    from tinyimg import read
    read('example.jpg').denoise().rescale(256, 256).rotate(45).write('output.png')

This style of programming is used a lot in some communities e.g. :term:`jQuery`
and some :term:`Java` and :term:`PHP` projects. This is unusual in Python
and not entirely clear if appropriate. Instead a Python programmer could
typically code like that::

    from tinyimg import read
    image = read('example.jpg')
    image.denoise()
    image.rescale(256, 256)
    image.rotate(45)
    image.write('output.png')

Tinyimg allows both styles or mixture of them. By default all methods that can
be chained are chainable. It's up to you what you choose. One of the down sides
of chaining is that when an exception occurs it can be not immediately clear
where it comes from when you call one method several times on one line. If you want to
explicitly forbid chaining you can do so by injection environment variable
`TINYIMG_NO_CHAINS` with non-false value before importing :mod:`tinyimg`. When
you do so methods that were previously chainable return ``None``::

    from os import environ
    environ['TINYIMG_NO_CHAINS'] = '1'
    
    from tinyimg import read
    # chaining explicitely disabled above
    
    image = read('example.jpg')
    image.blur(3).rotate(45)  # this raises an Exception

or from shell:

.. code-block:: bash

    $ TINYIMG_NO_CHAINS=1 python helloworld.py

Behind the scenes
=================

Tinyimg uses :term:`ImageMagick` :term:`DLL` to perform its operation.
Specifically :term:`MagickWand` API is used which is contained in
`libMagickWand.so`, `libMagickWand.dylib` or `libMagickWand.dll` depending on
the platform used. Tinyimg searches for the library in several places starting
from the place where bundled binaries are normally stored and ending with
system-wide locations. The details of search algorithms are detailed in
:ref:`search-path`. Resolved library is loaded through :term:`ctypes` and all
tinyimg API calls are translated into their several C API low-level
counterparts abstracting details for you. Tinyimg can work with
:term:`ImageMagick` version 6.5.9.0 or later but more recent versions are
bundled and advised to use.
