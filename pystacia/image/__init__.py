# coding: utf-8
# pystacia/image.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import division

""":class:`Image` creation and management operations"""


def _instantiate(factory):
    """Return new image object
       
       Not to be used directly.
    """
    return registry.get('image_factory', override=factory)()


def read(filename, factory=None):
    """Read :class:`Image` from filename.
       
       :param filename: file name to read
       :type filename: ``str``
       :param factory: Image subclass to use when instantiating objects
       :rtype: :class:`Image`
       
       Reads file, determines its format and returns an :class:`Image`
       representing it. You can optionally pass factory parameter
       to use alternative :class:`Image` subclass.
       
       >>> read('example.jpg')
       <Image(w=512,h=512,8bit,rgb,truecolor) object at 0x10302ee00L>
    """
    if not exists(filename):
        template = formattable('No such file or directory: {0}')
        raise IOError((2, template.format(filename)))
    
    return call(io.read, filename, factory=factory)


def read_blob(blob, format=None,  # @ReservedAssignment
              length=None, factory=None):
    """Read :class:`Image` from a blob string or stream with a header.
       
       :param blob: blob data string or stream
       :type blob: ``str`` (Python 2.x) / ``bytes`` (Python 3.x) or
         file-like object
       :param format: container format such as :term:`JPEG` or :term:`BMP`
       :type format: ``str``
       :param length: read maximum this bytes from stream
       :type length: ``int``
       :param factory: Image subclass to use when instantiating objects
       :rtype: :class:`Image`
       
       Reads image from string or data stream that contains a valid file
       header i.e. it carries information on image dimensions, bit depth and
       compression. Data format is equivalent to e.g. :term:`JPEG` file
       read into string(Python 2.x)/bytes(PYthon 3.x) or file-like object.
       It is useful in cases when you have open file-like object but not the
       file itself in the filesystem. That often happens in web applications
       which map :term:`POST` data with file-like objects. Format and length
       are typically not used but can be a hint when the information cannot be
       guessed from the data itself. You can optionally pass factory parameter
       to use alternative :class:`Image` subclass.
       
       >>> with file('example.jpg') as f:
       >>>     img = read_blob(f)
       >>> img
       <Image(w=512,h=512,8bit,rgb,truecolor) object at 0x10302ee00L>
    """
    if hasattr(blob, 'read'):
        blob = blob.read(length)
    
    return call(io.read_blob, blob, format, factory)


def read_raw(raw, format, width, height,  # @ReservedAssignment
             depth, factory=None):
    """Read :class:`Image` from raw string or stream.
       
       :param raw: raw data string or stream
       :type raw: ``str`` (Python 2.x) / ``bytes`` (Python 3.x) or
         file-like object
       :param format: raw pixel format eg. ``'RGB'``
       :type format: ``str``
       :param width: width of image in raw data
       :type width: ``int``
       :param height: height of image in raw data
       :type height: ``int``
       :param depth: depth of a single channel in bits
       :type depth: ``int``
       :param factory: Image subclass to use when instantiating objects
       :rtype: :class:`Image`
       
       Reads image data from a raw string or stream containing data in format
       such as :term:`RGB` or :term:`YCbCr`. The contained image has
       dimensions of width and height pixels. Each channel is of depth bits.
       You can optionally pass factory parameter to use alternative
       :class:`Image` subclass.
    
       >>> img = read_raw(b'raw triplets', 'rgb', 1, 1, 8)
    """
    return call(io.read_raw, raw, format, width, height, depth, factory)

from pystacia.common import Resource
from pystacia.image._impl import alloc, clone, free


class Image(Resource):
    _api_type = 'image'
    
    _alloc = alloc
    
    _clone = clone
    
    _free = free
    
    def _set_state(self, key, value, enum=None):
        if enum:
            value = enum_lookup(value, enum)
            
        simple_call(self, ('set', key), value)
        
    def _get_state(self, key, enum=None):
        value = simple_call(self, ('get', key))
            
        if enum:
            value = enum_reverse_lookup(enum, value)
            
        return value
    
    def write(self, filename, format=None,  # @ReservedAssignment
              compression=None, quality=None, flatten=None, background=None):
        """Write an image to filesystem.
           
           :param filename: file name to write to.
           :type filename: ``str``
           :param format: file format
           :type format: ``str``
           :param compression: compression algorithm
           :type compression: :class:`pystacia.lazyenum.EnumValue`
           :param quality: output quality
           :type quality: ``int``
           
           Saves an image to disk under given filename, format is determined
           from filename unless specified explicitely. The interpretation of
           quality parameter depends on the chosen format. E.g. for
           :term:`JPEG` it's a integer number between 1 (worst) and 100 (best)
           whilst for lossless format like
           :term:`PNG` 0 means best compression. The default value is to choose
           best available compression that preserves good quality image.
           
           >>> img = blank(10, 10)
           >>> img.write('example.jpg')
           >>> img.close()
           
           This method can be chained.
        """
        call(io.write, self, filename, format, compression,
             quality, flatten, background)
    
    def get_blob(self, format, compression=None,  # @ReservedAssignment
                 quality=None, factory=None):
        """Return a blob representing an image
           
           :param format: format of the output such as :term:`JPEG`
           :type format: ``str``
           :param compression: compression supported by format
           :type compression: :class:`pystacia.lazyenum.EnumValue`
           :param quality: output quality
           :rtype: ``str`` (Python 2.x) / ``bytes`` (Python 3.x)
           
           Returns blob carrying data representing an image along its header
           in the given format. Compression is one of compression algorithms.
           Some formats like :term:`TIFF` supports more then one compression
           algorithms but typically this parameter is not used.
           The interpretation of quality parameter depends
           on the chosen format. E.g. for :term:`JPEG` it's integer number
           between 1 (worst) and 100 (best) whilst for lossless format like
           :term:`PNG` 0 means best compression. The default value is to choose
           best available compression that preserves good quality image.
        """
        blob = call(io.get_blob, self, format, compression, quality)
        
        if factory:
            blob = factory(blob)
            
        return blob
        
    def get_raw(self, format, factory=None):  # @ReservedAssignment
        """Return ``dict`` representing raw image data.
           
           :param format: format of the output such as :term:`RGB`
           :type format:  ``str``
           :rtype: ``dict``
           
           Returns raw data ``dict`` consisting of raw, format, width, height
           and depth keys along their values.
        """
        return dict(raw=self.get_blob(format, factory),
                    format=format,
                    width=self.width,
                    height=self.height,
                    depth=self.depth)
        
    def rescale(self, width=None, height=None,
               factor=None, filter=None, blur=1):  # @ReservedAssignment
        """Rescales an image to given dimensions.
        
           :param width: Width of resulting image
           :type width: ``int``
           :param height: Height of resulting image
           :type height: ``int``
           :param factor: Zoom factor
           :type factor: ``float`` or ``tuple`` of ``float``
           :param filter: Scaling filter
           :type filter: :class:`pystacia.lazuenym.Enums`
           
           Rescales an image to a given width and height pixels. If one of the
           dimensions is set to ``None`` it gets automatically computed using
           the other one so that the image aspect ratio is preserved. Instead
           of supplying width and height you can use factor parameter which is
           a tuple of two floats specifying scaling factor along x and y axes.
           You can also pass single float as factor which implies the same
           factor for both axes. Filter is one of possible scaling algorithms.
           You can choose from popular :term:`Bilinear`, :term:`Cubic`,
           :term:`Sinc`, :term:`Lanczos` and many more. By default it uses
           filter which is most adequate for the scaling you perform i.e. the
           one which preserves as much as possible detail and sharpness.
           
           >>> img = read('example.jpg')
           >>> img.size
           (32L, 32L)
           >>> img.rescale(640, 480)
           >>> img.size
           (640L, 480L)
           >>> img.rescale(factor=.5)
           >>> img.size
           (320L, 240L)
           
           This method can be chained.
        """
        call(geometry.rescale, self, width, height, factor, filter, blur)
    
    def fit(self, width=None, height=None, mode=None, upscale=False, 
            filter=None, blur=1):  # @ReservedAssignment
        """Fits an image into a rectangle preserving aspect ratio
           
           :param width: width in pixels
           :type width: ``int``
           :param height: height in pixels
           :type height: ``int``
           
           Fits an image into a region of width, and height pixels
           preserving aspect ratio.
           
           This method can be chained.
        """
        call(geometry.fit, self, width, height, mode, upscale, filter, blur)
    
    def resize(self, width, height, x=0, y=0):
        """Resize (crop) image to given dimensions.
           
           :param width: Width of resulting image
           :type width: ``int``
           :param height: Height of resulting image
           :type height: ``int``
           :param x: x origin of resized area
           :type x: ``int``
           :param y: y origin of resixed area
           :type y: ``int``
           
           Crops out the given x, y, width, height area of image.
           
           >>> img = read('example.jpg')
           >>> img.size
           (512L, 512L)
           >>> img.resize(320, 240, 10, 20)
           >>> img.size()
           (320L, 240L)
           
           This method can be chained.
        """
        call(geometry.resize, self, width, height, x, y)
    
    def rotate(self, angle):
        """Rotate an image.
        
           :param angle: angle of rotation in degrees clockwise
           
           Rotates an image clockwise. Resulting image can be larger in size
           than the original. The resulting empty spaces are filled with
           transparent pixels.
           
           This method can be chained
        """
        call(geometry.rotate, self, angle)
        
    def flip(self, axis):
        """Flip an image along given axis.
           
           :param axis: X or Y axis
           :type axis: :class:`pystacia.lazyenum.EnumValue`
           
           Flips (mirrors) an image along :attr:`axes.x` or :attr:`axes.y`.
           
           This method can be chained.
        """
        call(geometry.flip, self, axis)
    
    def transpose(self):
        """Transpose an image.
           
           Creates a vertical mirror image by reflecting the
           pixels around the central x-axis while rotating them 90-degrees.
           In other words each row of source image from top to bottom becomes
           a column of new image from left to right.
           
           This method can be chained.
        """
        call(geometry.transpose, self)
    
    def transverse(self):
        """Transverse an image.
           
           Creates a horizontal mirror image by reflecting the
           pixels around the central y-axis while rotating them 270-degrees.
           
           This method can be chained.
        """
        call(geometry.transverse, self)
    
    def skew(self, offset, axis=None):
        """Skews an image by given offsets.
        
           :param offset: offset in pixels along given axis
           :type offset: ``int``
           :param axis: axis along which to perform skew
           :type axis: ``pystacia.lazyenum.EnumValue``
           
           Skews an image along given axis. If no axis is given it defaults
           to X axis.
           
           This method can be chained.
        """
        call(geometry.skew, self, offset, axis)
    
    def roll(self, x, y):
        """Roll pixels in the image.
           
           :param x: offset in the x-axis direction
           :type x: ``int``
           :param y: offset in the y-axis direction
           :type y: ``int``
        
           Rolls pixels in the image in the left-to-right direction along
           x-axis and top-to-bottom direction along y-axis. Offsets can be
           negative to roll in the opposite direction.
           
           This method can be chained.
        """
        call(geometry.roll, self, x, y)
    
    def straighten(self, threshold):
        """Attempt to straighten image.
           
           :param threshold: Separate background from foreground.
           :type threshold: ``float``
           
           Removes skew from the image. Skew is an artifact that occurs in
           scanned images because of the camera being misaligned,
           imperfections in the scanning or surface, or simply because
           the paper was not placed completely flat when scanned.
           
           This method can be chained.
        """
        call(geometry.straighten, self, threshold)
    
    def trim(self, similarity=.1, background=None):
        """Attempt to trim off extra background around image.
           
           :param similarity: Smilarity factor
           :type similarity: ``float``
           :param background: background color, transparent by default
           :type background: :class:`pystacia.color.Color`
           
           Removes edges that are the background color from the image.
           The greater similarity the more distant hues are considered the same
           color. Simlarity of `0` means only this exact color.
           
           This method can be chained.
        """
        call(geometry.trim, self, similarity, background)
    
    def chop(self, x, y, width, height):
        call(geometry.chop, self, x, y, width, height)
    
    def brightness(self, factor):
        """Brightens an image.
           
           :param factor: Brightness factor betwwen -1 and 1
           :type factor: ``float``
           
           Brightens an image with specified factor. Factor of ``0`` is
           no-change operation. Values towards ``-1`` make image darker.
           ``-1`` makes image completely black. Values towards 1 make image
           brigther. ``1`` makes image completely white.
           
           This method can be chained.
        """
        call(color_impl.brightness, self, factor)
    
    def contrast(self, factor):
        """Change image contrast.
           
           :param factor: Contrast factor betwwen -1 and 1
           :type factor: ``float``
           
           Change image contrast with specified factor. Factor of ``0`` is
           no-change operation. Values towards ``-1`` make image less
           contrasting. ``-1`` makes image completely gray. Values towards
           ``1`` increase image constrast. ``1`` pulls channel values towards
           0 and 1 resulting in a highly contrasting posterized image.
           
           This method can be chained.
        """
        call(color_impl.contrast, self, factor)
    
    def gamma(self, gamma):
        """Apply gamma correction to an image.
           
           :param gamma: Gamma value
           :type gamma: ``float``
           
           Apply gamma correction to an image. Value ``1`` is an identity
           operation. Higher values yield brighter image and lower values
           darken image. More information on gamma corection can be found
           here: http://en.wikipedia.org/wiki/Gamma_correction.
           
           This method can be chained
        """
        call(color_impl.gamma, self, gamma)
    
    def auto_gamma(self):
        """Auto-gamma image.
        
           Extracts the 'mean' from the image and adjust the
           image to try make set its gamma appropriatally.
           
           This method can be chained.
        """
        call(color_impl.auto_gamma, self)
    
    def auto_level(self):
        """Auto-level image.
        
           Adjusts the levels of an image by scaling the minimum and
           maximum values to the full quantum range.
           
           This method can be chained.
        """
        call(color_impl.auto_level, self)
    
    def modulate(self, hue=0, saturation=0, lightness=0):
        """Modulate hue, saturation and lightness of the image
           
           :param hue: Hue value from -1 to 1
           :type hue: ``float``
           :param saturation: Saturation value from -1 to infinity
           :type saturation: ``float``
           :param lightness: Lightness value from -1 to inifinity
           :type lightness: ``float``
           
           Setting any of the parameters to 0 is no-change operation.
           Hue parameter represents hue rotation relatively to current
           position. `-1` means rotation by 180 degrees counter-clockwise and
           1 is rotation by 180 degrees clockwise. Setting saturation to ``-1``
           completely desaturates image (makes it grayscale) while values from
           ``0`` towards infinity make it more saturated. Setting lightness
           to ``-1`` makes image completely black and values from ``0`` towards
           infinity make it lighter eventually reaching pure white.
           
           This method can be chained.
        """
        call(color_impl.modulate, self, hue, saturation, lightness)
    
    def desaturate(self):
        """Desatures an image.
           
           Reduces saturation level of all pixels to minimum yielding
           grayscale image.
           
           This method can be chained.
        """
        self.modulate(saturation=-1)
        
    def colorize(self, color):
        """Colorize image.
           
           :param color: color from which hue value is used
           :type color: :class:`pystacia.color.Color`
           
           Colorizes image resulting in image containing
           only one hue value.
           
           This method can be chained.
        """
        overlay = blank(self.width, self.height, color)
        
        self.overlay(overlay, composite=composites.colorize)
        
        overlay.close()
    
    def sepia(self, threshold=.8, saturation=-.4):
        """Sepia-tonne an image.
           
           :param threshold: Controls hue. Set to sepia tone by default.
           :type threshold: ``float``
           :param saturation: Saturation level
           :type saturation:``float``
           
           Perform sepia-tonning of an image. You can control hue by
           adjusting threshold parameter.
           
           This method can be chained.
        """
        call(color_impl.sepia, self, threshold, saturation)
    
    def equalize(self):
        """Equalize image histogram.
           
           This method usually increases the global contrast of many images,
           especially when the usable data of the image is represented by
           close contrast values. Through this adjustment, the intensities
           can be better distributed on the histogram. This allows for areas
           of lower local contrast to gain a higher contrast. See also:
           http://en.wikipedia.org/wiki/Histogram_equalization.
           
           This method can be chained.
        """
        call(color_impl.equalize, self)
    
    def normalize(self):
        """Normalize image histogram."""
        call(color_impl.normalize, self)
    
    def invert(self, only_gray=False):
        """Invert image colors.
           
           Inverts all image colors resulting in a negative image.
           
           This method can be chained.
        """
        call(color_impl.invert, self, only_gray)
    
    def solarize(self, factor):
        """Solarizes an image.
           
           :param factor: solarize factor
           :type factor: ``float``
           
           Applies solarization which is a color value opration similar to
           what can be a result of partially exposing a photograph in a
           darkroom. The usable range of factor is from ``0`` to ``1``
           inclusive. Value of ``0`` is no-change operation whilst ``1``
           produces a negative. Typically factor ``0.5`` produces
           interesting effect.
           
           This method can be chained.
        """
        call(color_impl.solarize, self, factor)
    
    def posterize(self, levels, dither=False):
        """Reduces number of colors in the image.
           
           :param levels: Output number of levels per channel
           :type levels: ``int``
           :param dither: Weather dithering should be performed
           'type dither: :bool:
           
           Reduces the image to a limited number of color levels.
           Levels specify color levels allowed in each channel. The
           channel spectrum is divided equally by level. Very low
           values (2, 3 or 4) have the most visible effect. ``1`` produces
           ``1**3`` output colors, ``2`` produces ``2**3`` colors ie. ``8``
           and so on. Setting dither to ``True`` enables dithering.
           
           This method can be chained.
        """
        call(color_impl.posterize, self, levels, dither)
    
    def threshold(self, factor=0.5, mode=None):
        """Threshold image forcing pixels into black & white.
        
           :param factor: Threshold factor
           :type factor: ``float`` or ``tuple``
           :patam mode: One of 'default', 'white', 'black'
           
           Threshold image resulting in black & white image. Factor specify
           lightness threshold. It's a float ranging from 0 to 1 and
           defaults to 0.5. Pixels
           below intensivity factor are renderer black and pixels
           above it end up white. In white mode channel pixels above factor
           intensivity are pushed into their maximum whilst one below are
           left untouched. In black mode channel pixels below factor are
           set to ``0`` whilst one above are left untouched. In random mode
           factor should be two-element tuple that specify minimum and maximum
           thresholds. Thresholds are then randomly chosen for each pixel
           individually from given range.
        """
        call(color_impl.threshold, self, factor, mode)
    
    def map(self, lookup, interpolation=None):  # @ReservedAssignment
        """Map image using intensivities as keys and lookup image.
           
           :param lookup: Lookup table image
           :type lookup: :class:`pystacia.image.Image`
           :param interpolation: interpolation method
           
           Maps an image using lightness as key and copying color values
           from lookup image.
        """
        call(color_impl.map, self, lookup, interpolation)
    
    def contrast_stretch(self, black=0, white=1):
        """Strech image contrast"""
        call(color_impl.contrast_stretch, self, black, white)
    
    def evaluate(self, operation, value):
        """Apply operation to imaget color information
           
           :param operation: Operation like "multiply" or "subtract"
           :type operation: Enum ``operations`` representation
           :param value: A constant value used as operand
           :type value: ``float``
           
           Evaluate each pixel in image with operation and provided value.
           E.g. using ``'divide'`` operation and ``2`` as value would result
           in all pixels divided by two.
        """
        call(color_impl.evaluate, self, operation, value)
    
    @property
    def total_colors(self):
        """Return total number of unique colors in image"""
        return self._get_state('colors')
    
    def get_range(self):
        """Return range minimum and maximum range of channels
           
           :rtype: ``tuple``
           
           Return a range of color information as a tuple of floats between
           0 and 1. E.g. black and white image woudle have a range
           of 0 for minimum and 1 for maximum
           1-color images will have maximum equal to minimum.
        """
        return call(color_impl.get_range, self)
    
    def blur(self, radius, strength=None):
        """Blur image.
           
           :param radius: Gaussian operator radius
           :type radius: float
           :param strength: Standard deviation (sigma)
           :type strength: float
           
           Convolves the image with a gaussian operator of the given radius
           and standard deviation (strength).
           
           This method can be chained.
        """
        call(blur_impl.blur, self, radius, strength)
    
    def motion_blur(self, radius, angle=0, strength=None, bias=None):
        """Motion blur image
           
           :param radius: Blur radius in pixels
           :type radius: ``float``
           :param angle: Angle measured clockwise to X-axis
           :type angle:``float``
           
           Applies motion blur of given radius along in given direction
           measured in degrees of X-axis clockwise.
           
           This method can be chained.
        """
        call(blur_impl.motion_blur, self, radius, angle, strength, bias)
    
    def gaussian_blur(self, radius, strength=None, bias=None):
        """Gaussian blur an image
           
           :param radius: radius in pixels
           :type radius: ``float``
           
           Applies gaussian blur to an image of given radius.
           
           This method can be chained.
        """
        
        call(blur_impl.gaussian_blur, self, radius, strength, bias)
    
    def adaptive_blur(self, radius, strength=None, bias=None):
        """Adaptive blur an image
           
           :param radius: radius in pixels
           :type radius: ``float``
           
           Applies adaptive blur of given radius to an image.
           
           This method can be chained.
        """
        call(blur_impl.adaptive_blur, self, radius, strength, bias)
        
    def adaptive_sharpen(self, radius, strength=None, bias=None):
        """Adaptive sharpen an image
           
           :param radius: radius in pixels
           :type radius: ``float``
           
           Applies adaptive sharpening to an image.
           
           This method can be chained.
        """
        call(blur_impl.adaptive_sharpen, self, radius, strength, bias)
    
    def detect_edges(self, radius, strength=None):
        """Detect edges in image.
           
           :param radius: radius of detected edges
           :type radius: ``float``
           
           Analyzes image and marks contrasting edges. It operates on
           all channels by default so it might be a good idea to grayscale
           an image before performing it.
           
           This method can be chained.
        """
        call(blur_impl.detect_edges, self, radius, strength)
    
    #TODO: moving center here
    def radial_blur(self, angle):
        """Performs radial blur.
        
           :param angle: Blur angle in degrees
           :type angle: ``float``
           
           Radial blurs image within given angle.
           
           This method can be chained.
        """
        call(blur_impl.radial_blur, self, angle)
    
    def sharpen(self, radius, strength=None, bias=None):
        """Sharpen an image.
           
           :param radius: Radius of sharpening kernel
           :type radius: ``float``
           
           Performs sharpening of an image.
           
           This method can be chained.
        """
        call(blur_impl.sharpen, self, radius, strength, bias)
    
    def denoise(self):
        """Attempt to remove noise preserving edges.
        
           Applies a digital filter that improves the quality of a
           noisy image.
           
           This method can be chained.
        """
        call(blur_impl.denoise, self)
    
    def despeckle(self):
        """Attempt to remove speckle preserving edges.
           
           Resulting image almost solid color areas are smoothed preserving
           edges.
           
           This method can be chained.
        """
        call(blur_impl.despeckle, self)
    
    def emboss(self, radius=0, strength=None):
        """Apply edge detecting algorithm.
           
           :param radius: filter radius
           :type radius: ``int``
           :param stregth: filter strength (sigma)
           :type strength: ``int``
           
           On a typical photo creates effect of raised edges.
           
           This method can be chained.
        """
        call(blur_impl.emboss, self, radius, strength)
    
    def swirl(self, angle):
        """Distort image with swirl effect.
           
           :param angle: Angle in degrees clockwise
           :type angle: ``float``
           
           Swirls an image by angle clockwise. Angle can be negative resulting
           in distortion in opposite direction.
           
           This method can be chained.
        """
        call(deform.swirl, self, angle)
    
    def wave(self, amplitude, length, offset=0, axis=None):
        """Apply wave like distortion to an image.
           
           :param amplitude: amplitude (A) of wave in pixels
           :type amplitude: ``int``
           :param length: length (lambda) of wave in pixels.
           :type length: ``int``
           :param offset: offset (phi) from initial position in pixels
           :type length: ``int``
           :param axis: axis along which to apply deformation. Defaults to x.
           :type axis: ``pystacia.enum.EnumValue``
           
           Applies wave like distoration to an image along chosen
           axis. Axis defaults to :attr:``axes.x``. Offset parameter is
           not effective as for now. Will be implemented in the feature.
           Resulting empty areas are filled with transparent pixels.
           
           This method can be chained.
        """
        call(deform.wave, self, amplitude, length, offset, axis)
    
    def sketch(self, radius, angle=45, strength=None):
        """Simulate sketched image.
           
           :param radius: stroke length.
           :type radius: ``float``
           :param angle: angle of strokes clockwise relative to horizontal axis
           :type radius: ``float``
           :param strength: effect strength (sigma)
           :type strength: ``float``
           
           Simulates a sketch by adding strokes into an image.
           
           This method can be chained.
        """
        call(special.sketch, self, radius, angle, strength)
    
    def add_noise(self, attenuate=0, noise_type=None):
        """Add noise to an image.
           
           :param attenuate: Attenuation factor
           :type attenuate: ``float``
           :param noise_type: values representing
           :attr:`pystacia.image.enum.noises`
           
           Adds noise of given type to an image. Noise type defaults
           to ``"gaussian"``.
           
           This method can be chained.
        """
        call(special.add_noise, self, attenuate, noise_type)
    
    def charcoal(self, radius, strength=None, bias=None):
        """Simluate a charcoal.
           
           :param radius: Charcoal radius
           :type radius: ``float``
           
           This method can be chained.
        """
        call(special.charcoal, self, radius, strength, bias)
    
    def oil_paint(self, radius):
        """Simulates oil paiting.
           
           :param radius: brush radius
           :type radius: ``float``
           
           Each pixel is replaced by the most frequent color occurring in a
           circular region defined by radius.
           
           This method can be chained.
        """
        call(special.oil_paint, self, radius)
    
    def shade(self, azimuth=45, elevation=45, grayscale=True):
        """Simulate 3D shading effect.
           
           :param azimuth: azimuth in degrees - light direction
           :type azimuth: ``float``
           :param elevation: elevation above image surface in degrees
           :type elevation: ``float``
           :param grayscale: Whether grayscale image
           :type grayscale: ``bool``
           
           Simulates 3D effect by finding edges and rendering them as rised
           with light comming from azimuth direction in elevation degrees above
           image surface. Azimuth is rotation along Z axis. By default it
           grayscales an image before applying an effect.
           
           This method can be chained
        """
        call(special.shade, self, azimuth, elevation, grayscale)
    
    def spread(self, radius):
        """Spread pixels in random direction.
           
           :param radius: Maximal distance from original position
           :type radius: ``int``
           
           Applies special effect method that randomly displaces each
           pixel in a block defined by the radius parameter.
        
           This method can be chained.
        """
        call(special.spread, self, radius)
    
    def dft(self, magnitude=True, factory=None):
        """Applies inverse discrete Fourier transform to an image.
           
           :param magnitude: if ``True``, return as magnitude / phase pair
             otherwise a real / imaginary image pair.
           :type magnitude: ``bool``
           :rtype: 2-element ``tuple`` of :class:`Image`
           
           Performs inverse discrete Fourier transform (DFT)
           and returns a tuple of two resulting images. Go to
           http://www.imagemagick.org/Usage/fourier/ to see what can be
           accomplished with it. This method will not be present if your
           ImageMagick installation wasn't compiled against FFTW.
        """
        return call(special.dft, self, magnitude, factory)
    
    def fx(self, expression):  # @ReservedAssignment
        """Perform expression using ImageMagick mini-language.
        
           :param expression: expression to evaluate
           
           For more information on the available expressions visit:
           http://www.imagemagick.org/script/fx.php.
           
           This method can be chained.
        """
        return call(special.fx, self, expression)
    
    def get_pixel(self, x, y, factory=None):
        """Get pixel color at given coordinates.
           
           :param x: x coordinate of pixel
           :type x: ``int``
           :param y: y coordinate of pixel
           :type y: ``int``
           :rtype: :color:`pystacia.color.Color`
           
           Reads pixel color at point ``(x,y)``.
        """
        return call(pixel.get_pixel, self, x, y, factory)

    
    def fill(self, fill, blend=1):
        """Overlay color over whole image.
           
           :param fill: color to overlay
           :type fill: :class:`pystacia.color.Color`
           :param blend: overlay blending
           :type blend: ``float``
           
           Overlay a color over whole image. Blend is bleding factor of a
           color with `0` being completely transparent and ``1`` fully opaque.
           
           This method can be chained.
        """
        call(pixel.fill, self, fill, blend)
    
    def set_color(self, fill):
        """Fill whole image with one color.
        
           :param fill: desired fill color
           :type fill: :class:`pystacia.color.Color`
           
           Fills whole image with a monolithic color.
           
           >>> img = read('example.jpg')
           >>> img.fill(color.from_string('yellow'))
           >>> img.get_pixel(20, 20) == color.from_string('yellow')
           True
           
           This method can be chained.
        """
        call(pixel.set_color, self, fill)
    
    def set_alpha(self, alpha):
        """Set alpha channel of pixels in the image.
        
           :param alpha: target alpha value
           :type alpha: float
           
           Resets alpha channel of all pixels in the image to given
           value between 0 (transpanret) and 1 (opaque).
           
           This method can be chained.
        """
        call(pixel.set_alpha, self, alpha)
    
    def overlay(self, image, x=0, y=0, composite=None):
        """Overlay another image on this image.
        
           :param image: imaged to be overlayed
           :type image: :class:`pystacia.image.Image`
           :param x: x coordinate of overlay
           :type x: ``int``
           :param y: y coordinate of overlay
           :type y: ``int``
           :param composite: Composition operator
           :type composite: :class:`pystacia.lazyenum.EnumValue`
           
           Overlays given image on this image at ``(x, y)`` using
           composite operator. There are many popular composite
           operators available like lighten, darken, colorize, saturate,
           overlay, burn or default - over.
           
           >>> img = read('example.jpg')
           >>> img2 = read('example2.jpg')
           >>> img.overlay(img2, 10, 10)
           
           This method can be chained.
        """
        call(pixel.overlay, self, image, x, y, composite)
    
    def compare(self, image, metric=None, factory=None):
        """Compare image to another image
           
           :param image: reference image
           :type image: :class:`pystacia.image.Image`
           :param metric: distortion metric
           :type metric: :class:`pystacia.lazyenum.EnumValue`
           :param factory: factory to be used to create difference image
           :rtype: ``tuple`` of :class:`Image` and ``float`` distortion in
            given metric
            
            Compares two images of the same sizes. Returns a tuple of an
            image marking different parts with red color and a distortion
            metric.
            By default it uses :attr:`pystacia.image.metrics.absolute_error`
            metric. If images are of  differnt sizes
            returns ``False`` instead.
        """
        return call(pixel.compare, self, image, metric, factory)
    
    def is_same(self, image):
        """Check if images are the same.
           
           :param image: reference image
           :rtype: ``bool``
           
           Returns ``True`` if images are exactly the same i.e.
           are of same dimensions
           and underlying pixel data is exactly the same.
        """
        result = self.compare(image)
        
        return result and result[1] == 0
    
    #def shadow(self, radius, x=0, y=0, opacity=0.5):
    #    resource = self.resource
    #    guard(resource,
    #          lambda: cdll.MagickShadowImage(resource, opacity,
    #                                         radius, x, y))
    
    def splice(self, x, y, width, height):
        """Insert bands of transprent areas into an image.
           
           :param x: x coordinate of splice
           :type x: ``int``
           :param y: y coordinate of splice
           :type y: ``int``
           :param width: width of splice
           :type width: ``int``
           :param height: height of splice
           :type height: ``int``
           
           This method can be chained.
        """
        call(geometry.splice, self, x, y, width, height)
    
    def __colorspace():  # @NoSelf
        doc = (  # @UnusedVariable
        """Return or set colorspace associated with image.
           
           Sets or gets colorspace. When you set this property there's no
           colorspace conversion performed and the original channel values
           are just left as is. If you actually want to perform a conversion
           use :attr:`convert_colorspace` instead. Popular colorspace include
           RGB, YCbCr, grayscale and so on.
           
           :rtype: :class:`pystacia.lazyenum.EnumValue`
        """)
        
        def fget(self):
            return self._get_state('colorspace', enum=colorspaces)
        
        def fset(self, value):
            self._set_state('colorspace', value, enum=colorspaces)
        
        return property(**locals())
    
    colorspace = __colorspace()
    
    def __type():  # @ReservedAssignment @NoSelf
        doc = (  # @UnusedVariable
        """Set or get image type.
           
           :rtype: :class:`pystacia.lazyenum.EnumValue`
           
           Popular image types include truecolor, pallete, bilevel and their
           matter counterparts.
           
           >>> img = read('example.jpg')
           >>> img.type == types.truecolor
        """)
        
        def fget(self):
            return self._get_state('type', enum=types)
        
        def fset(self, value):
            self._set_state('type', value, enum=types)
            
        return property(**locals())
    
    type = __type()  # @ReservedAssignment
    
    def convert_colorspace(self, colorspace):
        """Convert to given colorspace.
           
           :param colorspace: destination colorspace
           :type colorspace: :class:`pystacia.color.Color`
           
           Converts an image to a given colorspace.
           
           >>> img = read('example.jpg')
           >>> img.convert_colorspace(colorspace.ycbcr)
           >>> img.colorspace == colorspace.ycbcr
           True
           
           This method can be chained.
        """
        call(color_impl.convert_colorspace, self, colorspace)
    
    @property
    def width(self):
        """Get image width.
           
           :rtype: ``int``
           
           Return image width in pixels.
        """
        return self._get_state('width')
    
    @property
    def height(self):
        """Get image height.
           
           :rtype: ``int``
           
           Return image height in pixels.
        """
        return self._get_state('height')
    
    @property
    def size(self):
        """Return a tuple of image width and height.
           
           :rtype: ``tuples`` of two ``int``
           
           Returns a tuple storing image width on first position and image
           height on second position.
           
           >>> img = read('example.jpg')
           >> img.size
           (640, 480)
        """
        return (self.width, self.height)
    
    def __depth():  # @NoSelf
        doc = (  # @UnusedVariable
        """Set or get image depth per channel.
        
           :rtype: ``int``
           
           Set or get depth per channel in bits. Either 8 or 16.
        """)
        
        def fget(self):
            return self._get_state('depth')
        
        def fset(self, value):
            return self._set_state('depth', value)
            
        return property(**locals())
    
    depth = __depth()
    
    def show(self, no_gui=False):
        """Display an image in GUI.
           
           :param no_gui: Skip opening interactive viewer program
           :type no_gui: ``bool``
           
           :rtype: ``str``
           
           Saves image to temporary lossless file format on a disk and sends
           it to default image handling program to display. Returns a path
           to the temporary file. You get no gurantees about life span of a
           file after process ended since it will be typically deleted when
           process ends.
        """
        extension = 'bmp'
        if 'png' in magick.get_formats():
            extension = 'png'
            
        tmpname = mkstemp()[1] + '.' + extension
        self.write(tmpname)
        if not no_gui:
            webbrowser.open('file://' + tmpname)
        
        return tmpname
    
    def checkerboard(self):
        """Fills transparent pixels with checkerboard.
           
           Useful for presentation when you want to explicitely
           mark transparent pixels when otherwise it might be
           unclear where they are.
        """
        background = checkerboard(*self.size)
        
        self.overlay(background, composite=composites.dst_over)
        
        background.close()

    def __repr__(self):
        template = '<{class_}(w={w},h={h},{depth}bit'\
                   ',{colorspace},{type}) object at {addr}>'
        w, h = self.size
        depth, type = self.depth, self.type.name  # @ReservedAssignment
        colorspace, addr = self.colorspace.name, id(self)  # @ReservedAssignment
        class_ = self.__class__.__name__
        
        return formattable(template).format(class_=class_, w=w, h=h,
                                            depth=depth, colorspace=colorspace,
                                            addr=addr, type=type)


from pystacia import registry

registry._install_default('image_factory', Image)  # @UndefinedVariable

import webbrowser
from tempfile import mkstemp
from os import environ
from os.path import exists

from pystacia.compat import formattable
from pystacia import color
color_module = color
from pystacia.api.func import call, simple_call
from pystacia import magick
from pystacia.api.enum import (lookup as enum_lookup,
                               reverse_lookup as enum_reverse_lookup)

#if not 'fftw' in magick.get_delegates():
del Image.dft

try:
    disable_chains = environ['PYSTACIA_NO_CHAINS']
except KeyError:
    disable_chains = False
    
if not disable_chains:
    # perform chainability
    from pystacia.util import chainable
    
    for key in (key for key in Image.__dict__ if not key.startswith('_')):
        item = Image.__dict__[key]
        if callable(item) and item.__doc__ and ':rtype:' not in item.__doc__:
            setattr(Image, key, chainable(item))


from pystacia.image.generic import blank  # prevent circular references
from pystacia.image._impl import (io, geometry, color as color_impl,
                                 blur as blur_impl, deform, special, pixel)

# convenience imports
from pystacia.image.enum import (types, filters, colorspaces,  # @UnusedImport
                                 compressions, composites, axes, noises,
                                 thresholds, fit_modes)
from pystacia.image.generic import (checkerboard, noise,  # @UnusedImport
                                    plasma)
from pystacia.image.sample import (lena, magick_logo, rose,  # @UnusedImport
                                   wizard, granite, netscape)
