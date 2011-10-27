===================
Working with images
===================

The :class:`tinyimg.image.Image` is a central concept to the whole library.
Though you typically don't use its constructor directly and rely on factories.
All the functionality is implemented in :mod:`tinyimg.image` module but for
convenience reasons attributes are imported to main :mod:`tinyimg` module from
where you would import it.

Reading and writing
===================

To read a file from the disk you would use :func:`tinyimg.image.read` factory::

    from tinyimg import read
    
    image = read('example.jpg')

This reads file `example.jpg` from current working directory and returns
:class:`tinyimg.image.Image` instance. To write it back to disk under different
name and format you could write::

    image.write('output.png')

This would save it back to `output.png` file with format `PNG`. Format is
determined from the file extension.

Sometimes instead of having your data stored in a file you already have it
in byte string or stream (file-like object with :meth:`read` method). In such
case you use :func:`tinyimg.image.read_blob` instead::

     from tinyimg import read_blob
     
     # data is byte string or stream in e.g. PNG format
     image = read_blob(data)

Tinyimg can also deal with :term:`RAW` uncompressed data. You
use :func:`tinyimg.image.read_raw` method in such cases. Note that you need to
explicitly specify :term:`RAW` format, width, height and depth per channel as
it's not carried along data itself.

::

    from tinyimg import read_raw
    
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
analogical to parameters you would pass to :meth:`tinyimg.image.read_raw` you 
can call :meth:`tinyimg.image.get_raw` passing it color space::

    image.get_raw('ycbcr')

Common properties
=================

Dimensions
----------

All images have some common properties like dimensions, color space, type and
depth. To get dimensions of the image you can access :attr:`tinyimg.Image.size`
property to get ``(width, height)`` tuple or :attr:`tinyimg.Image.width` and
:attr:`tinyimg.Image.height` separately:

>>> image.size
(640, 480)
>>> image.width
640
>>> image.height
480

Color space
-----------

Color space represents combination of channels that image is internally stored
in. You can query it with :attr:`tinyimg.Image.colorspace` property. It yields
`tinyimg.image.colorspaces.rgb` for most images but other values are also 
possible.

>>> image.colorspace
tinyimg.lazyenum.enum('colorspace').rgb

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
representation use :meth:`tinyimg.image.Image.convert_colorspace` method instead.

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

You can read and set types with :attr:`tinyimg.Image.type` property.
Setting a type which loses color information relative to original results
in automatic :term:`dithering`:

>>> image.type
tinyimg.lazyenum.enum('type').truecolor

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
into :meth:`tinyimg.image.Image.rescale`:

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
:meth:`tinyimg.image.Image.resize`. it accepts four parameters describing cropped
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

Color transformation
====================

Bluring, denoising and enahncing
--------------------------------

Deforming
---------

Special effects
---------------

Bundled standard images
-----------------------