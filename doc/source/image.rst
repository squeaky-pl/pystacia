===================
Working with images
===================

The :class:`pystacia.image.Image` is a central concept to the whole library.
Though you typically don't use its constructor directly and rely on factories.
All the functionality is implemented in :mod:`pystacia.image` module but for
convenience reasons attributes are imported to main :mod:`pystacia` module from
where you would import it.

Reading and writing
===================

Files, streams and byte strings
-------------------------------

To read a file from the disk you would use :func:`pystacia.image.read` factory::

    from pystacia import read
    
    image = read('example.jpg')

This reads file `example.jpg` from current working directory and returns
:class:`pystacia.image.Image` instance. To write it back to disk under different
name and format you could write::

    image.write('output.png')

This would save it back to `output.png` file with format `PNG`. Format is
determined from the file extension.

Sometimes instead of having your data stored in a file you already have it
in byte string or stream (file-like object with :meth:`read` method). In such
case you use :func:`pystacia.image.read_blob` instead::

     from pystacia import read_blob
     
     # data is byte string or stream in e.g. PNG format
     image = read_blob(data)

Pystacia can also deal with :term:`RAW` uncompressed data. You
use :func:`pystacia.image.read_raw` method in such cases. Note that you need to
explicitly specify :term:`RAW` format, width, height and depth per channel as
it's not carried along data itself.

::

    from pystacia import read_raw
    
    # create 2x2 pixel RGB image with red, green, blue and black pixel
    # from RGB triplets in 8 bit depth
    data = [255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0]
    data = bytes(data) # python 3k, ''.join(chr(x) for x in data) in 2.x
    
    image = read_raw(data, 'rgb', 2, 2, 8)

Sometimes you may also want to dump image object contents to byte string instead
of saving in to this. You use get_blob method to do so. To dump image contents
as PNG blob you would call::

    image.get_blob('png')

To get :term:`RAW` data along its format, dimensions, and depth as dictionary
analogical to parameters you would pass to :meth:`pystacia.image.read_raw` you 
can call :meth:`pystacia.image.get_raw` passing it color space::

    image.get_raw('ycbcr')

Generic images
--------------

Instead of reading an image from a file or stream you sometimes may want to
start from blank image or well defined pattern.

Use :func:`pystacia.image.blank` to create empty blank image of given
dimensions. By default it fills it with transparent pixels, but a third parameter
specifying color can be used.

>>> from pystacia import blank, color
>>> blank(100, 100)
>>> blank(100, 100, color.from_string('red'))
>>> blank(100, 100, color.from_rgba(0, 1, 0, 0.5))

.. container:: clearfix left

    .. figure:: _static/generated/transparent.jpg
       
       Transparent (default)
    
    .. figure:: _static/generated/red.jpg
       
       Red
       
    .. figure:: _static/generated/green.jpg
       
       Translucent green

You can also generate a checkerboard pattern which is used in this documentation
to mark transparent pixels with :func:`pystacia.image.checkerboard` which
accepts width and height.

>>> from pystacia import checkerboard
>>> checkerboard(200, 200)

.. figure:: _static/generated/checkerboard.png
       
   Checkerboard pattern

Common properties
=================

Dimensions
----------

All images have some common properties like dimensions, color space, type and
depth. To get dimensions of the image you can access :attr:`pystacia.Image.size`
property to get ``(width, height)`` tuple or :attr:`pystacia.Image.width` and
:attr:`pystacia.Image.height` separately:

>>> image.size
(640, 480)
>>> image.width
640
>>> image.height
480

Color space
-----------

Color space represents combination of channels that image is internally stored
in. You can query it with :attr:`pystacia.Image.colorspace` property. It yields
`pystacia.image.colorspaces.rgb` for most images but other values are also 
possible.

>>> image.colorspace
pystacia.lazyenum.enum('colorspace').rgb

You can also assign to this property. It results in reinterpretation of stored
color space i.e. if the original image was in :term:`RGB` color space assigning
it :term:`YCbCr` would result in treating `Red channel` as `Luma` and `Green`
and `Blue` information as `Chroma components` which yields strange
visual effects.

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original :term:`RGB` image
    
    .. figure:: _static/generated/lena_ycbcr.jpg
       
       Reinterpreted as :term:`YCbCr`
       
    .. figure:: _static/generated/lena_cmy.jpg
       
       Reinterpreted as :term:`CMY`

Note that :term:`RGB` image reinterpreted as :term:`CMY` is simply negative
since `CMY` is subtractive model complementing `RGB` i.e. each channel value is
inversion of its counterpart.

If you want to change (convert) underlying color space without affecting visual
representation use :meth:`pystacia.image.Image.convert_colorspace` method instead.

Depth
-----

Depth represents number of bits used to store channel information. It's
typically 8 bit for :term:`TrueColor` images but can be as well 16 bit
for some :term:`TIFF` images. You query the image depth with
:attr:`pystacia.image.Image.depth` property.

>>> image.depth
8

Storage type
------------

Another aspect of image storing is a type. Type of image relates to how the
values stored in memory are mapped into color values on the screen.
Sometimes it's a direct mapping like :term:`TrueColor` where values stored in
:term: `RGB` triplets directly encode their visual representation.
Another popular type are paletted (indexed) images where image consist of abstract values
(typically 0 to 255) that are translated into final color value through a lookup
table (:term:`palette`). This has been popularized with :term:`GIF` format.
:term:`Grayscale` image is an image storing only luminosity information (also
typically in one byte). It can be also taught as a indexed image with implied
palette which maps each luminosity (l) value into an :term:`RGB` triplet
(l, l, l). Finally bilevel image is an image consisting of two colors - typically
black and white stored in one bit per pixel.

Each of types mentioned above also has its :term:`matte` counterpart i.e.
one that is accompanied by alpha channel. These have additional ``_matte`` suffix.

You can read and set types with :attr:`pystacia.Image.type` property.
Setting a type which loses color information relative to original results
in automatic :term:`dithering`:

>>> image.type
pystacia.lazyenum.enum('type').truecolor

>>> image.type = types.palette

>>> image.type = types.grayscale

>>> image.type = types.bilevel

Here are close-ups of resulting images:

.. container:: clearfix left

    .. figure:: _static/generated/lena_closeup.jpg
       
       :term:`TrueColor` image
    
    .. figure:: _static/generated/lena_palette.png
       
       Converted to :term:`pallette`
       
    .. figure:: _static/generated/lena_gray.jpg
       
       Coverted to :term:`grayscale`
       
    .. figure:: _static/generated/lena_bilevel.png
       
       Coverted to :term:`bilevel`

Geometry transformation
=======================

Rescaling
---------

Rescaling is an operation of changing size of original image
that preserves all the original visual characteristics in the new
viewport. Rescaling can be both proportional and not proportional.
You typically perform this operation by suppling width and height
into :meth:`pystacia.image.Image.rescale`:

>>> image.size
(256, 256)
>>> image.rescale(300, 200)
>>> image.size
(300, 200)
>>> image.rescale(128, 128)
>>> image.size
(128, 128)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
    
    .. figure:: _static/generated/lena_rescale_300.jpg
       
       (100, 200)
       
    .. figure:: _static/generated/lena_rescale_128.jpg
       
       (128, 128)

Alternatively you can pass factor into method. This specifies how many times
the original sizes are multiplied. If you pass single number the scaling will
be proportional in both dimensions. You can also pass a two-element ``tuple``.

>>> image.rescale(factor=0.75)
>>> image.rescale(factor=(0.6, 0.5))
>>> image.rescale(factor=(1.3, 1))

.. container:: clearfix left

    .. figure:: _static/generated/lena_rescale_f0.75.jpg
       
       Factor 0.75
    
    .. figure:: _static/generated/lena_rescale_f0.6_0.5.jpg
       
       Factor (0.6, 0.5)
       
    .. figure:: _static/generated/lena_rescale_f1.3_1.jpg
       
       Factor (1.3, 1)

Note that this way resulting size is calculated relatively to previous size.

Another interesting aspect of resizing is resize filter. This affects the
sharpness or smoothness and quality of rescaled image. Typically used filters
include :term:`point` (also known as nearest neighbor), :term:`cubic`,
:term:`sinc` or :term:`lanczos`.


>>> image.rescale(factor=2, filter=filters.point)

>>> image.rescale(factor=2, filter=filters.cubic)

>>> image.rescale(factor=2, filter=filters.sinc)

>>> image.rescale(factor=2, filter=filters.lanczos)

Upscaling close-ups with differnt filters:

.. container:: clearfix left

    .. figure:: _static/generated/lena_upscale_point.jpg
       
       Point
    
    .. figure:: _static/generated/lena_upscale_cubic.jpg
       
       Cubic
       
    .. figure:: _static/generated/lena_upscale_sinc.jpg
       
       Sinc
       
    .. figure:: _static/generated/lena_upscale_lanczos.jpg
       
       Lanczos


>>> image.rescale(factor=0.5, filter=filters.point)

>>> image.rescale(factor=0.5, filter=filters.cubic)

>>> image.rescale(factor=0.5, filter=filters.sinc)

>>> image.rescale(factor=0.5, filter=filters.lanczos)

Downscaling close-ups with different filters:

.. container:: clearfix left

    .. figure:: _static/generated/lena_downscale_point.jpg
       
       Point
    
    .. figure:: _static/generated/lena_downscale_cubic.jpg
       
       Cubic
       
    .. figure:: _static/generated/lena_downscale_sinc.jpg
       
       Sinc
       
    .. figure:: _static/generated/lena_downscale_lanczos.jpg
       
       Lanczos

Resizing
--------

If you wanna crop out a portion of an image you can use
:meth:`pystacia.image.Image.resize`. it accepts four parameters describing cropped
out region: width, height, x and y in this order. The latter two default
to 0:

>>> image.size
(256, 256)

>>> image.resize(128, 128)

>>> image.resize(64, 128, 128, 128)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_resize1.jpg
       
       (128, 128)
    
    .. figure:: _static/generated/lena_resize2.jpg
       
       (64, 128, 128, 128)

Rotating
--------

You can rotate an image with :meth:`pystacia.image.Image.rotate` method.
Angle is mesaured in degrees. Positive
angles yield clockwise rotation while negative ones counter-clockwise.
The resulting empty spaces are filled with transparent pixels.

>>> image.rotate(30)

>>> image.rotate(90)

>>> image.rotate(-45)

.. container:: clearfix left

    .. figure:: _static/generated/lena128.jpg
       
       Original
       
    .. figure:: _static/generated/lena_rotate30.jpg
       
       30°
       
    .. figure:: _static/generated/lena_rotate90.jpg
       
       90°
       
    .. figure:: _static/generated/lena_rotate-45.jpg
       
       -45°

Flipping
--------

Use :meth:`pystacia.image.Image.flip` to flip (mirror) image around
X or Y axis. Use :attr:`pystacia.image.Image.axes` enumeration to
specify axis.

>>> image.flip(axes.x)

>>> image.flip(axes.y)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_flipx.jpg
       
       Mirror X
       
    .. figure:: _static/generated/lena_flipy.jpg
       
       Mirror Y

Transposing and transversing
---------------------------

Use :meth:`pystacia.image.Image.transpose` and
:meth:`pystacia.image.Image.transverse` to transpose
or transverse an image. Transposing creates a vertical mirror image by reflecting the
pixels around the central x-axis while rotating them 90-degrees. Transversing
creates a horizontal mirror image by reflecting the
pixels around the central y-axis while rotating them 270-degrees.

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_transpose.jpg
       
       Transposed
       
    .. figure:: _static/generated/lena_transverse.jpg
       
       Transversed
       
Skewing
_______

Skewing is the action of pushing one of the edges of an image along X or Y
axis. You can perform it with :meth:`pystacia.image.Image.skew` passing
offset in pixels and desired axis.

>>> image.skew(10, axes.x)

>>> image.skew(-5, axes.x)

>>> image.skew(20, axes.y)

.. container:: clearfix left

    .. figure:: _static/generated/lena128.jpg
       
       Original
       
    .. figure:: _static/generated/lena_skewx10.jpg
       
       10 pixels along X
       
    .. figure:: _static/generated/lena_skewx-5.jpg
       
       -5 pixels along X
       
    .. figure:: _static/generated/lena_skewy20.jpg
       
       20 pixels along Y

Rolling
-------

Rolling in an action of offsetting an image and filling empty space
with pixels that overflew on the edge. It can be performed with
:meth:`pystacia.image.Image.roll` method. It accepts offses in X and Y
directions as arguments.

>>> image.roll(100, 0)

>>> image.roll(-30, 40)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_roll100_0.jpg
       
       Rolled by (100, 0)
       
    .. figure:: _static/generated/lena_roll-30_40.jpg
       
       Rolled by (-30, 40)

Straightening image
-------------------

Sometimes you have an image that is not straightened since It could be scanned
so. You can use :meth:`pystacia.image.Image.straighten` to correct that.
It accepts single parameter - threshold which tells Pystacia what is the
difference between baackground and subject.

>>> image.straighten(20)

.. container:: clearfix left

    .. figure:: _static/generated/lena_notstraight.jpg
       
       Rotated image
       
    .. figure:: _static/generated/lena_straightened.jpg
       
       Straightened up

Trimming extra background
-------------------------

If your image has extra background around it you can trim it off with
:meth:`pystacia.image.Image.trim` method. It accepts two optional parameters
similarity and background color of space to discard (defaults to transparent).

>>> image.trim()

.. container:: clearfix left

    .. figure:: _static/generated/lena_extrabg.jpg
       
       Image with empty space
       
    .. figure:: _static/generated/lena_trim.jpg
       
       Trimmed off

Color transformation
====================

Color transformations are operations that affect color channel information
without changing pixel location in any way.

Adjsuting contrast
------------------

:meth:`pystacia.image.Image.contrast` increases or decreases contrast of an image.
Passing `0` is no change operation. Values towards `-1` decrease
constract whilst values towards `1` increase it.

>>> image.contrast(-1)

>>> image.contrast(-0.6)

>>> image.contrast(-0.25)

>>> image.contrast(0)

>>> image.contrast(0.25)

>>> image.contrast(0.75)

>>> image.contrast(1)

.. container:: clearfix left

    .. figure:: _static/generated/lena_contrast-1.jpg
       
       -1
       
    .. figure:: _static/generated/lena_contrast-0.6.jpg
       
       -0.6
       
    .. figure:: _static/generated/lena_contrast-0.25.jpg
       
       -0.25
       
    .. figure:: _static/generated/lena128.jpg
       
       0 (original)
       
    .. figure:: _static/generated/lena_contrast0.25.jpg
       
       +0.25
       
    .. figure:: _static/generated/lena_contrast1.jpg
       
       +1


Adjusting brightness
--------------------

:meth:`pystacia.image.Image.brightness` adjusts the brightness of an image.
Value `0` is no-change operation. Values towards `-1` make image darker whilst
calues towards `1` increase brightness.

>>> image.brightness(-1)

>>> image.brightness(-0.6)

>>> image.brightness(-0.25)

>>> image.brightness(0)

>>> image.brightness(0.25)

>>> image.brightness(0.75)

>>> image.brightness(1)

.. container:: clearfix left

    .. figure:: _static/generated/lena_brightness-1.jpg
       
       -1
       
    .. figure:: _static/generated/lena_brightness-0.6.jpg
       
       -0.6
       
    .. figure:: _static/generated/lena_brightness-0.25.jpg
       
       -0.25
       
    .. figure:: _static/generated/lena128.jpg
       
       0 (original)
       
    .. figure:: _static/generated/lena_brightness0.25.jpg
       
       +0.25
       
    .. figure:: _static/generated/lena_brightness0.75.jpg
       
       +0.75

Gamma correction
----------------

You can use :meth:`pystacia.image.Image.gamma` to apply gamma correction. Value
of `1` is no-change operation. Values towards `0` make image darker. Values
towards infinity make image lighter.

>>> image.gamma(0.3)

>>> image.gamma(0.6)

>>> image.gamma(1)

>>> image.gamma(1.5)

>>> image.gamma(2)

.. container:: clearfix left

    .. figure:: _static/generated/lena_gamma0.1.jpg
       
       0.1
       
    .. figure:: _static/generated/lena_gamma0.3.jpg
       
       0.3
       
    .. figure:: _static/generated/lena_gamma0.6.jpg
       
       0.6
       
    .. figure:: _static/generated/lena128.jpg
       
       1 (Original)
       
    .. figure:: _static/generated/lena_gamma1.5.jpg
       
       1.5
       
    .. figure:: _static/generated/lena_gamma2.jpg
       
       2

Modulation
----------

Modulation is an operation of adjusting hue, saturation and luminance of
an image. It can be accomplished with :meth:`pystacia.image.Image.modulate`.
It accepts parameters in hue, saturation and luminance order. They all default
to 0 meaning no change. Usable hue values start from -1 meaning rotation of hue
by -180 degrees to 1 meaning +180 degrees. Saturation values towards `-1` 
desaturte image whilst values towards infinity saturate it. Setting luminosity
to `-1` yields completely black image whilst values towards infinity make it
brighter.

>>> image.modulate(-1, -0.25, 0.1)

>>> image.modulate(-0.5, 0.25, 0)

>>> image.modulate(-0.2, 0.5, -0.25)

>>> image.modulate(0, 0, 0)

>>> image.modulate(0.4, -0.5, 0)

>>> image.modulate(0.8, 0, 0)

.. container:: clearfix left

    .. figure:: _static/generated/lena_modulate-1,-0.25,0.1.jpg
       
       (-1, -0.25, 0.1)
       
    .. figure:: _static/generated/lena_modulate-0.5,0.25,0.jpg
       
       (-0.5, 0.25, 0)
       
    .. figure:: _static/generated/lena_modulate-0.2,0.5,-0.25.jpg
       
       (-0.2, 0.5, -0.25)
       
    .. figure:: _static/generated/lena128.jpg
       
       (0, 0, 0) Original
       
    .. figure:: _static/generated/lena_modulate0.4,-0.5,0.jpg
       
       (0.4, -0.5, 0)
       
    .. figure:: _static/generated/lena_modulate0.8,0,0.jpg
       
       (0.8, 0, 0)

Desaturation
------------

You can peform desaturation with :meth:`pystacia.image.Image.desaturate`. It is
a shortcut to :meth:`pystacia.image.Image.modulate` passing `-1` as saturation.

>>> image.desaturate()

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_desaturate.jpg
       
       Desatured

Colorization
------------

Colorization in an action of replacing all hue values in an image with a hue
from a given color. :meth:`pystacia.image.Image.colorize` accepting single color
parameter performs it.

>>> image.colorize(color.from_string('red'))

>>> image.colorize(color.from_string('yellow'))

>>> image.colorize(color.from_string('blue'))

>>> image.colorize(color.from_string('violet'))

>>> image.colorize(color.from_string('green'))

.. container:: clearfix left

    .. figure:: _static/generated/lena128.jpg
       
       Original
       
       
    .. figure:: _static/generated/lena_colorize_red.jpg
       
       red
       
    .. figure:: _static/generated/lena_colorize_yellow.jpg
       
       yellow
       
    .. figure:: _static/generated/lena_colorize_blue.jpg
       
       blue
       
    .. figure:: _static/generated/lena_colorize_violet.jpg
       
       violet

Sepia tone
----------

:meth:`pystacia.image.Image.sepia` performs effect similar to old-fashined
sepia image. You can adjust hue and saturation parameters but the default
values are a good starting point.

>>> image.sepia()

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_sepia.jpg
       
       Sepia tonning

Equalization
------------

:meth:`pystacia.image.Image.equalize` is a method of streching channel information
to fill full avaiable spectrum. It can result in drastic color quality improvement
on low contrast, tainted images.

>>> image.equalize()

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_equalize.jpg
       
       Equalized image

Invertion
---------

Invertion is a process of substractin original channel value from it's maximum
value. It results in a negative and can be performed with
:meth:`pystacia.image.Image.invert`.

>>> image.negative()

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_invert.jpg
       
       Inverted image

Solarization
------------

Solarization leads to effect similar of partly exposing an image in a darkroom.
It can be performed with :meth:`pystacia.image.Image.solarize`. It accepts single
parameter - factor. Factor `0` is no change operation, Factor `1` is exactly the
same as negative of original. Value of `0.5` yields particulary interesting effects.

>>> image.solarize(0)

>>> image.solarize(0.5)

>>> image.solarize(1)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       0 (Original)
       
    .. figure:: _static/generated/lena_solarize0.5.jpg
       
       0.5
       
    .. figure:: _static/generated/lena_solarize1.jpg
       
       1 (Inverted original)

Posterization
-------------

:meth:`pystacia.image.Image.posterize` accepts single level parameter and
reduces number of colors in the image
to ``levels ** 3`` colors. Each channel has level final values distributed
equally along its spectrum. So 1 level yields 1 color, 2 levels yield 8 color
and so on.

>>> image.posterize(2)

>>> image.posterize(3)

>>> image.posterize(4)

>>> image.posterize(5)

.. container:: clearfix left

    .. figure:: _static/generated/lena128.jpg
       
       Original
       
    .. figure:: _static/generated/lena_posterize2.jpg
       
       2 levels
       
    .. figure:: _static/generated/lena_posterize3.jpg
       
       3 levels
       
    .. figure:: _static/generated/lena_posterize4.jpg
       
       4 levels
       
    .. figure:: _static/generated/lena_posterize5.jpg
       
       5 levels

Bluring, denoising and enhancing
================================

Blur
----

You can blur image with :meth:`pystacia.image.Image.blur`. Method accepts
mandatory radius and optional strength parameter.

>>> img.blur(3)

>>> img.blur(10)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_blur3.jpg
       
       radius 3
       
    .. figure:: _static/generated/lena_blur10.jpg
       
       radius 10
       
Radial blur
-----------

To perform radial blur use :meth:`pystacia.image.Image.radial_blur`. Pass in
single parameter - blur angle in degrees.

>>> img.blur(10)

>>> img.blur(45)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_radial_blur10.jpg
       
       10 degrees
       
    .. figure:: _static/generated/lena_radial_blur45.jpg
       
       45 degrees
       
Removing noise
--------------

If you want to perform noise removal you can use
:meth:`pystacia.image.Image.denoise` method.

>>> img.denoise()

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_denoise.jpg
       
       Denoised image

Removing speckles
-----------------

:meth:`pystacia.image.Image.despeckle` on the other hand removes speckles
- larger grain defects than noise.

>>> img.despeckle()

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_despeckle.jpg
       
       Despeckled image


Embossing
---------

Emboss raises detected edges in image creating 3D effect sharpening it at
the same time.
Call :meth:`pystacia.image.Image.emboss` to use it.

>>> img.emboss()

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_emboss.jpg
       
       Embossed image

Deforming
=========

Swirling
--------

To apply whirlpool like effect use :meth:`pystacia.image.Image.swirl`. Positive
angles result in clockwise whirling, negative in counter-clockwise.

>>> img.swirl(60)

>>> img.swirl(-30)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_swirl60.jpg
       
       60 degrees
       
    .. figure:: _static/generated/lena_swirl-30.jpg
       
       -30 degrees

Waving
------

:meth:`pystacia.image.Image.wave` applies sinusoidal deformation along give axis
(defaults to x).
You can control amplitude and length of the wave. Resulting extra pixels are
transparent.

>>> img.wave(20, 100)

>>> img.wave(-10, 50)

>>> img.wave(50, 200 axis=axes.y)

>>> img.wave(10, 30, axis=axes.y)

.. container:: clearfix left

    .. figure:: _static/generated/lena128.jpg
       
       Original
       
    .. figure:: _static/generated/lena_wave20,100,x.jpg
       
       (100, 20, x)
       
    .. figure:: _static/generated/lena_wave-10,50,x.jpg
       
       (50, -10, x)
       
    .. figure:: _static/generated/lena_wave50,200,y.jpg
       
       (200, 50, y)
       
    .. figure:: _static/generated/lena_wave10,30,y.jpg
       
       (30, 10, y)

Special effects
===============

Sketch effect
-------------

You can use :meth:`pystacia.image.Image.sketch` to simulate sketch effect.
You can control the effect with two parameters radius of strokes and angle of
pencils (defaults to 45 degrees).

>>> image.sketch(3)

>>> image.sketch(6, 0)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_sketch3.jpg
       
       radius 3, angle 45
       
    .. figure:: _static/generated/lena_sketch6,0.jpg
       
       radius 6, angle 0

Oil paint effect
----------------

:meth:`pystacia.image.Image.oil_paint` simulates oil painting by covering image
with circles filled with mean color value. It accepts single paramater -
radius in pixels.

>>> image.oil_paint(3)

>>> image.oil_paint(8)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_oil_paint3.jpg
       
       radius 2
       
    .. figure:: _static/generated/lena_oil_paint8.jpg
       
       radius 8

Spreading
---------

:meth:`pystacia.image.Image.spread` fuzzes and image with pixel displacement
within given radius.

>>> image.spread(3)

>>> image.spread(6)

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_spread2.jpg
       
       radius 2
       
    .. figure:: _static/generated/lena_spread6.jpg
       
       radius 6

Fx method
---------

With :meth:`pystacia.image.Image.fx` you can perform custom operations using
:term:`ImageMagick` tiny scripting language. Beware that this can be very
slow on large images as it's directly interpreted and not compiled in any way.
http://www.imagemagick.org/script/fx.php has infomration on syntax.

>>> image.fx('u * 1/2')

.. container:: clearfix left

    .. figure:: _static/generated/lena.jpg
       
       Original
       
    .. figure:: _static/generated/lena_fx.jpg
       
       After processing

Pixel manipulation
==================

Reading single pixels
---------------------

To access pixel data anywhere in the image you cen use 
:meth:`pystacia.image.Image.get_pixel` passing it x and y
coordinates.

>>> image.get_pixel(128, 128)
<Color(r=0.9396,g=0.5933,b=0.4317,a=1) object at 0x108002200L>

Filling
-------

If you want to fill image with solid color you use
:meth:`pystacia.image.Image.fill` passing it color. You can
optionally pass also blend parameter specyfing opacity with
`1` meaning opaque.

>>> image.fill(color.from_string('red'))

>>> image.fill(color.from_string('green'), 0.5)

>>> image.fill(color.from_string('blue'), 0.25)

>>> image.fill(color.from_string('orange'), 0.2)

.. container:: clearfix left

    .. figure:: _static/generated/lena128.jpg
       
       Original
       
    .. figure:: _static/generated/lena_fill_red.jpg
       
       red
       
    .. figure:: _static/generated/lena_fill_green.jpg
       
       green 0.5 blend
       
    .. figure:: _static/generated/lena_fill_blue.jpg
       
       blue 0.25 blend
       
    .. figure:: _static/generated/lena_fill_orange.jpg
       
       orange 0.2 blend

Setting color
-------------

Another way to paint over whole image is using
:meth:`pystacia.image.Image.set_color`. Unlinke :meth:`pystacia.image.fill` it always
discards backgorund information replacing pixels. You can use alpha component
of color to gain translucency.

>>> image.set_color(color.from_string('red'))

>>> image.set_color(color.from_rgba(0, 1, 0, 0.5))

>>> image.set_color(color.from_rgba(0, 0, 0, 0.2))

>>> image.set_color(color.from_rgba(1, 0, 1, 0.5))

.. container:: clearfix left

    .. figure:: _static/generated/lena128.jpg
       
       Original
       
    .. figure:: _static/generated/lena_set_color_red.jpg
       
       red
       
    .. figure:: _static/generated/lena_set_color_green.jpg
       
       green 0.5 alpha
       
    .. figure:: _static/generated/lena_set_color_black.jpg
       
       black 0.2 alpha
       
    .. figure:: _static/generated/lena_set_color_violet.jpg
       
       violet 0.5 alpha

Setting alpha
-------------

Sometimes you may want to override alpha level for all pixels at once. You
can do that with :meth:`pystacia.image.Image.set_alpha`.

>>> image.set_alpha(0.75)

>>> image.set_color(0.5)

>>> image.set_color(0.25)

>>> image.set_color(0)

.. container:: clearfix left

    .. figure:: _static/generated/lena128.jpg
       
       Original
       
    .. figure:: _static/generated/lena_alpha0.75.jpg
       
       0.75
       
    .. figure:: _static/generated/lena_alpha0.5.jpg
       
       0.5
       
    .. figure:: _static/generated/lena_alpha0.25.jpg
       
       0.25
       
    .. figure:: _static/generated/lena_alpha0.jpg
       
       0

Overlaying
----------

With :meth:`pystacia.image.Image.overlay` you can overlay images on top of
image the method is called from. It accepts the image that is going to be 
overlaid as first parameter, x and y coordinates and composite mode.
There are many composite modes available. `over` is the default one,
other popular ones include `colorize`, `multiply`, `overlay`, `pin_light`.

>>> image.overlay(other, 32, 32)

>>> image.overlay(other, 32, 32, composites.colorize)

>>> image.overlay(other, 32, 32, composites.multiply)

>>> image.overlay(other, 32, 32, composites.overlay)

>>> image.overlay(other, 32, 32, composites.pin_light)

>>> image.overlay(pther, 32, 32, composites.saturate)

.. container:: clearfix left

    .. figure:: _static/generated/lena128.jpg
       
       Original
       
    .. figure:: _static/generated/lena_overlay1.jpg
       
       Over (default)
       
    .. figure:: _static/generated/lena_overlay2.jpg
       
       colorize
       
    .. figure:: _static/generated/lena_overlay3.jpg
       
       multiply
       
    .. figure:: _static/generated/lena_overlay4.jpg
       
       overlay
       
    .. figure:: _static/generated/lena_overlay5.jpg
       
       pin_light
       
    .. figure:: _static/generated/lena_overlay6.jpg
       
       saturate
       
    .. figure:: _static/generated/lena_overlay7.jpg
       
       soft_light
       
    .. figure:: _static/generated/lena_overlay8.jpg
       
       modulus_add
       
    .. figure:: _static/generated/lena_overlay9.jpg
       
       modulus_substract
       
    .. figure:: _static/generated/lena_overlay10.jpg
       
       luminize
       
    .. figure:: _static/generated/lena_overlay11.jpg
       
       hard_light

Utilities
=========

Displaying on the screen
------------------------

When in GUI session you can display image in available image preview program
with :meth:`pystacia.image.Image.show`. The call is non-blocking meaning that
the control is immediately returned to your program

>>> image.show()

Marking transparent pixels
--------------------------

Sometimes it might be not clear from the context which pixels are translucent
and which are opaque. You can use :meth:`pystacia.image.Image.checkerboard` to
overlay your image on top of checkerboard pattern in the same manner that
:term:`Photoshop` does.

>>> image.checkerboard()

Bundled images
==============

pystacia comes with standard test images which can be used for testing purposes.
Most of them are embedded in :term:`ImageMagick` library.

:meth:`pystacia.lena` optionally accepting size parameter:

.. figure:: _static/generated/lena.jpg

:meth:`pystacia.magick_logo`:

.. figure:: _static/generated/magick_logo.jpg

:meth:`pystacia.rose`:

.. figure:: _static/generated/rose.jpg

:meth:`pystacia.wizard`

.. figure:: _static/generated/wizard.jpg

:meth:`pystacia.granite`

.. figure:: _static/generated/granite.jpg

:meth:`pystacia.netscape`

.. figure:: _static/generated/netscape.jpg


