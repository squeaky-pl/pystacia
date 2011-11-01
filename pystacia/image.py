# coding: utf-8
# pystacia/image.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import division

""":class:`Image` creation and management operations"""


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
    
    filename = b(filename)
    
    if not factory:
        factory = Image
    
    image = factory()
    
    guard(image.wand, lambda: cdll.MagickReadImage(image.wand, filename))
    
    return image


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
    
    if not factory:
        factory = Image
    
    image = factory()
    
    if format:
        # ensure we always get bytes
        format = b(format.upper())  # @ReservedAssignment
        old_format = cdll.MagickGetImageFormat(image.wand)
        template = formattable('Format "{0}" unsupported')
        guard(image.wand,
              lambda: cdll.MagickSetFormat(image.wand, format),
              template.format(format))
    
    guard(image.wand,
          lambda: cdll.MagickReadImageBlob(image.wand, blob, len(blob)))
    
    if format:
        guard(image.wand,
                  lambda: cdll.MagickSetFormat(image.wand, old_format))
    
    return image


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
    if hasattr(raw, 'read'):
        raw = raw.read()
    
    format = b(format.upper())  # @ReservedAssignment
    
    if not factory:
        factory = Image
    
    image = factory()
    
    guard(image.wand, lambda: cdll.MagickSetSize(image.wand, width, height))
    guard(image.wand, lambda: cdll.MagickSetDepth(image.wand, depth))
    guard(image.wand, lambda: cdll.MagickSetFormat(image.wand, format))
        
    guard(image.wand,
          lambda: cdll.MagickReadImageBlob(image.wand, raw, len(raw)))
    
    return image


def read_special(spec, width=None, height=None, factory=None):
    """Read special :term:`ImageMagick` image resource"""
    if not factory:
        factory = Image
        
    image = factory()
    
    if width and height:
        guard(image.wand, lambda:
              cdll.MagickSetSize(image.wand, width, height))
    
    spec = b(spec)
    
    guard(image.wand, lambda: cdll.MagickReadImage(image.wand, spec))
    
    return image


def checkerboard(width, height, factory=None):
    """Returns standard checkerboard image
      
       :param width: width  in pixels
       :type width: ``int``
       :param height: height in pixels
       :type height: ``int``
       :rtype: :class:`pystacia.image.Image` or factory
    """
    return read_special('pattern:checkerboard', width, height, factory)


def blank(width, height, background=None, factory=None):
    """Create :class:`Image` with monolithic background
       
       :param width: Width in pixels
       :type width: ``int``
       :param height: Height in pixels
       :type height: ``int``
       :param background: background color, defaults to fully transparent
       :type background: :class:`pystacia.Color`
       
       Creates blank image of given dimensions filled with background color.
       
       >>> blank(32, 32, color.from_string('red'))
       <Image(w=32,h=32,16bit,rgb,palette) object at 0x108006000L>
    """
    if not background:
        background = 'transparent'
    
    return read_special('xc:' + str(background), width, height, factory)

from pystacia.util import only_live


class Image(object):
    def __init__(self, wand=None):
        self.__wand = wand if wand else cdll.NewMagickWand()
        self.__closed = False
        
        _register_cleanup(self)
    
    @only_live
    def copy(self):
        """Create new independent copy of an image.
        
           :rtype: :class:`pystacia.image.Image`
        """
        wand = cdll.CloneMagickWand(self.__wand)
        
        return Image(wand)
    
    @only_live
    def write(self, filename, format=None,  # @ReservedAssignment
              compression=None, quality=None):
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
        if format:
            format = b(format.upper())  # @ReservedAssignment
            old_format = cdll.MagickGetImageFormat(self.__wand)
            template = formattable('Format "{0}" unsupported')
            guard(self.__wand,
                  lambda: cdll.MagickSetImageFormat(self.__wand, format),
                  template.format(format))
            
        if quality != None:
            old_quality = cdll.MagickGetImageCompressionQuality(self.__wand)
            guard(self.__wand,
                  lambda: cdll.MagickSetImageCompressionQuality(self.__wand,
                                                                quality))
        
        guard(self.__wand,
              lambda: cdll.MagickWriteImage(self.__wand, b(filename)))
        
        if quality != None:
            guard(self.__wand,
                  lambda: cdll.MagickSetImageCompressionQuality(self.__wand,
                                                                old_quality))
        if format:
            guard(self.__wand,
                  lambda: cdll.MagickSetImageFormat(self.__wand, old_format))
        
        return self
    
    @only_live
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
        if compression != None:
            old_compression = cdll.MagickGetImageCompression(self.__wand)
            compression = enum_lookup(compression)
            guard(self.__wand,
                  lambda: cdll.MagickSetImageCompression(self.__wand,
                                                    compression))
            
        if quality != None:
            old_quality = cdll.MagickGetImageCompressionQuality(self.__wand)
            guard(self.__wand,
                  lambda: cdll.MagickSetImageCompressionQuality(self.__wand,
                                                                quality))
            
        # ensure we always get bytes
        format = b(format.upper())  # @ReservedAssignment
        old_format = cdll.MagickGetFormat(self.__wand)
        template = formattable('Format "{0}" unsupported')
        guard(self.__wand,
              lambda: cdll.MagickSetFormat(self.__wand, format),
              template.format(format))
        
        size = c_size_t()
        result = guard(self.__wand,
                       lambda: cdll.MagickGetImageBlob(self.__wand,
                                                       byref(size)))
        blob = string_at(result, size.value)
        cdll.MagickRelinquishMemory(result)
        
        guard(self.__wand,
              lambda: cdll.MagickSetFormat(self.__wand, old_format))
        
        if quality != None:
            guard(self.__wand,
                  lambda: cdll.MagickSetImageCompressionQuality(self.__wand,
                                                                old_quality))
        if compression != None:
            guard(self.__wand,
                  lambda: cdll.MagickSetImageCompression(self.__wand,
                                                    old_compression))
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
        
    @only_live
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
           
           Rescales an image to a given width and height pixels. Instead of
           supplying width and height you can use factor parameter which is
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
        if not filter:
            filter = filters.undefined  # @ReservedAssignment
        
        if not width and not height:
            if not factor:
                template = 'Either width, height or factor must be provided'
                raise TinyException(template)
            
            width, height = self.size
            if not hasattr(factor, '__getitem__'):
                factor = (factor, factor)
            width, height = int(width * factor[0]), int(height * factor[1])
        
        value = enum_lookup(filter)
        
        guard(self.__wand,
              lambda: cdll.MagickResizeImage(self.__wand, width, height,
                                             value, blur))
    
    @only_live
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
        guard(self.__wand,
              lambda: cdll.MagickCropImage(self.__wand, width, height, x, y))
    
    @only_live
    def rotate(self, angle):
        """Rotate an image.
        
           :param angle: angle of rotation in degrees clockwise
           
           Rotates an image clockwise. Resulting image can be larger in size
           than the original. The resulting empty spaces are filled with
           transparent pixels.
           
           This method can be chained
        """
        guard(self.__wand,
              lambda: cdll.MagickRotateImage(self.__wand,
                                             color.transparent.wand, angle))
        
    @only_live
    def flip(self, axis):
        """Flip an image along given axis.
           
           :param axis: X or Y axis
           :type axis: :class:`pystacia.lazyenum.EnumValue`
           
           Flips (mirrors) an image along :attr:`axes.x` or :attr:`axes.y`.
           
           This method can be chained.
        """
        if axis.name == 'x':
            guard(self.__wand, lambda: cdll.MagickFlipImage(self.__wand))
        elif axis.name == 'y':
            guard(self.__wand, lambda: cdll.MagickFlopImage(self.__wand))
        else:
            raise TinyException('axis must be X or Y')
    
    @only_live
    def transpose(self):
        """Transpose an image.
           
           Creates a vertical mirror image by reflecting the
           pixels around the central x-axis while rotating them 90-degrees.
           In other words each row of source image from top to bottom becomes
           a column of new image from left to right.
           
           This method can be chained.
        """
        guard(self.__wand, lambda: cdll.MagickTransposeImage(self.__wand))
        
        return self
    
    @only_live
    def transverse(self):
        """Transverse an image.
           
           Creates a horizontal mirror image by reflecting the
           pixels around the central y-axis while rotating them 270-degrees.
           
           This method can be chained.
        """
        guard(self.__wand, lambda: cdll.MagickTransverseImage(self.__wand))
    
    @only_live
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
        if not axis:
            axis = axes.x
            
        if axis == axes.x:
            x_angle = degrees(atan(offset / self.height))
            y_angle = 0
        elif axis == axes.y:
            x_angle = 0
            y_angle = degrees(atan(offset / self.width))
            
        guard(self.__wand,
              lambda: cdll.MagickShearImage(self.__wand,
                                            color.transparent.wand,
                                            x_angle, y_angle))
    
    @only_live
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
        guard(self.__wand, lambda: cdll.MagickRollImage(self.__wand, x, y))
    
    @only_live
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
        guard(self.__wand,
              lambda: cdll.MagickDeskewImage(self.__wand, threshold))
    
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
        # TODO: guessing of background?
        background_free = not(background)
        if not background:
            background = color.from_string('transparent')
        
        # preserve background color
        old_color = color.Color()
        guard(self.__wand,
              lambda: cdll.MagickGetImageBackgroundColor(self.__wand,
                                                         old_color.wand))
        guard(self.__wand,
              lambda: cdll.MagickSetImageBackgroundColor(self.__wand,
                                                         background.wand))
        
        guard(self.__wand,
              lambda: cdll.MagickTrimImage(self.__wand, similarity * 100))
        
        #restore background color
        guard(self.__wand,
              lambda: cdll.MagickSetImageBackgroundColor(self.__wand,
                                                         old_color.wand))
        
        if background_free:
            background.close()
    
    @only_live
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
        guard(self.__wand,
              lambda: cdll.MagickBrightnessContrastImage(self.__wand,
                                                         factor * 100, 0))
    
    @only_live
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
        guard(self.__wand,
              lambda: cdll.MagickBrightnessContrastImage(self.__wand,
                                                         0, factor * 100))
    
    @only_live
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
        guard(self.__wand, lambda: cdll.MagickGammaImage(self.__wand, gamma))
    
    @only_live
    def auto_gamma(self):
        """Auto-gamma image.
        
           Extracts the 'mean' from the image and adjust the
           image to try make set its gamma appropriatally.
           
           This method can be chained.
        """
        guard(self.__wand,
              lambda: cdll.MagickAutoGammaImage(self.__wand))
    
    @only_live
    def auto_level(self):
        """Auto-level image.
        
           Adjusts the levels of an image by scaling the minimum and
           maximum values to the full quantum range.
           
           This method can be chained.
        """
        guard(self.__wand,
              lambda: cdll.MagickAutoLevelImage(self.__wand))
    
    @only_live
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
        guard(self.__wand,
              lambda: cdll.MagickModulateImage(self.__wand,
                                               lightness * 100 + 100,
                                               saturation * 100 + 100,
                                               hue * 100 + 100))
    
    def desaturate(self):
        """Desatures an image.
           
           Reduces saturation level of all pixels to minimum yielding
           grayscale image.
           
           This method can be chained.
        """
        self.modulate(saturation=-1)
        
    @only_live
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
    
    @only_live
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
        threshold = 2 ** int(magick.get_options()['QuantumDepth']) * threshold
        
        guard(self.__wand,
              lambda: cdll.MagickSepiaToneImage(self.__wand, threshold))
        
        if saturation:
            self.modulate(saturation=saturation)
    
    @only_live
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
        guard(self.__wand, lambda: cdll.MagickEqualizeImage(self.__wand))
    
    @only_live
    def invert(self, only_gray=False):
        """Invert image colors.
           
           Inverts all image colors resulting in a negative image.
           
           This method can be chained.
        """
        guard(self.__wand,
              lambda: cdll.MagickNegateImage(self.__wand, only_gray))
    
    @only_live
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
        factor = (1 - factor) * 2 ** magick.get_depth()
        
        guard(self.__wand,
              lambda: cdll.MagickSolarizeImage(self.__wand, factor))
    
    @only_live
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
        guard(self.__wand,
              lambda: cdll.MagickPosterizeImage(self.__wand, levels, dither))
    
    @only_live
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
        if strength == None:
            strength = radius
            
        guard(self.__wand,
              lambda: cdll.MagickBlurImage(self.__wand, radius, strength))
    
    @only_live
    #TODO: moving center here
    def radial_blur(self, angle):
        """Performs radial blur.
        
           :param angle: Blur angle in degrees
           :type angle: ``float``
           
           Radial blurs image within given angle.
           
           This method can be chained.
        """
        guard(self.__wand,
              lambda: cdll.MagickRadialBlurImage(self.__wand, angle))
    
    @only_live
    def denoise(self):
        """Attempt to remove noise preserving edges.
        
           Applies a digital filter that improves the quality of a
           noisy image.
           
           This method can be chained.
        """
           
        guard(self.__wand, lambda: cdll.MagickEnhanceImage(self.__wand))
    
    @only_live
    def despeckle(self):
        """Attempt to remove speckle preserving edges.
           
           Resulting image almost solid color areas are smoothed preserving
           edges.
           
           This method can be chained.
        """
        guard(self.__wand, lambda: cdll.MagickDespeckleImage(self.__wand))
    
    @only_live
    def emboss(self, radius=0, strength=None):
        """Apply edge detecting algorithm.
           
           :param radius: filter radius
           :type radius: ``int``
           :param stregth: filter strength (sigma)
           :type strength: ``int``
           
           On a typical photo creates effect of raised edges.
           
           This method can be chained.
        """
        if strength == None:
            strength = radius
            
        guard(self.__wand,
              lambda: cdll.MagickEmbossImage(self.__wand, radius, strength))
    
    @only_live
    def swirl(self, angle):
        """Distort image with swirl effect.
           
           :param angle: Angle in degrees clockwise
           :type angle: ``float``
           
           Swirls an image by angle clockwise. Angle can be negative resulting
           in distortion in opposite direction.
           
           This method can be chained.
        """
        guard(self.__wand, lambda: cdll.MagickSwirlImage(self.__wand, angle))
    
    @only_live
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
        if not axis:
            axis = axes.x
            
        transparent = color.from_string('transparent')
        
        old_color = color.Color()
        guard(self.__wand,
              lambda: cdll.MagickGetImageBackgroundColor(self.__wand,
                                                         old_color.wand))
        guard(self.__wand,
              lambda: cdll.MagickSetImageBackgroundColor(self.__wand,
                                                         transparent.wand))
        
        if axis.name == 'y':
            self.rotate(90)
        
        guard(self.__wand,
              lambda: cdll.MagickWaveImage(self.__wand, amplitude, length))
        
        if axis.name == 'y':
            self.rotate(-90)
        
        guard(self.__wand,
              lambda: cdll.MagickSetImageBackgroundColor(self.__wand,
                                                         old_color.wand))
        old_color.close()
        transparent.close()
    
    @only_live
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
        if strength == None:
            strength = radius
        guard(self.__wand,
              lambda: cdll.MagickSketchImage(self.__wand, radius,
                                             strength, angle))
    
    @only_live
    def oil_paint(self, radius):
        """Simulates oil paiting.
           
           :param radius: brush radius
           :type radius: ``float``
           
           Each pixel is replaced by the most frequent color occurring in a
           circular region defined by radius.
           
           This method can be chained.
        """
        guard(self.__wand,
              lambda: cdll.MagickOilPaintImage(self.__wand, radius))
    
    @only_live
    def spread(self, radius):
        """Spread pixels in random direction.
           
           :param radius: Maximal distance from original position
           :type radius: ``int``
           
           Applies special effect method that randomly displaces each
           pixel in a block defined by the radius parameter.
        
           This method can be chained.
        """
        guard(self.__wand, lambda: cdll.MagickSpreadImage(self.__wand, radius))
    
    @only_live
    def dft(self, magnitude=True):
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
        magnitude = bool(magnitude)
        copy = self.copy()
        
        guard(copy.wand,
            lambda: cdll.MagickForwardFourierTransformImage(copy.wand,
                                                           magnitude))
        
        first = blank(*self.size)
        second = blank(*self.size)
        
        first.overlay(copy, composite=composites.copy)
        
        guard(copy.wand, lambda: cdll.MagickNextImage(copy.wand))
        
        second.overlay(copy, composite=composites.copy)
        
        copy.close()
        
        return (first, second)
    
    @only_live
    def fx(self, expression):  # @ReservedAssignment
        """Perform expression using ImageMagick mini-language.
        
           :param expression: expression to evaluate
           
           For more information on the available expressions visit:
           http://www.imagemagick.org/script/fx.php.
           
           This method can be chained.
        """
        wand = guard(self.__wand,
                     lambda: cdll.MagickFxImage(self.__wand, b(expression)))
        cdll.DestroyMagickWand(self.__wand)
        self.__wand = wand
    
    @only_live
    def get_pixel(self, x, y):
        """Get pixel color at given coordinates.
           
           :param x: x coordinate of pixel
           :type x: ``int``
           :param y: y coordinate of pixel
           :type y: ``int``
           :rtype: :color:`pystacia.color.Color`
           
           Reads pixel color at point ``(x,y)``.
        """
        color = color_module.Color()
        
        guard(self.__wand,
              lambda: cdll.MagickGetImagePixelColor(self.__wand, x, y,
                                                    color.wand))
        
        return color
    
    @only_live
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
        # image magick ignores alpha setting of color
        # let's incorporate it into blend
        blend *= fill.alpha
        
        blend = color_module.from_rgb(blend, blend, blend)
        
        guard(self.__wand,
              lambda: cdll.MagickColorizeImage(self.__wand, fill.wand,
                                               blend.wand))
        
        blend.close()
    
    @only_live
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
        if hasattr(cdll, 'MagickSetImageColor'):
            guard(self.__wand,
                  lambda: cdll.MagickSetImageColor(self.__wand, fill.wand))
            
            # MagickSetImageColor doesnt copy alpha
            if fill.alpha != 1:
                self.set_alpha(fill.alpha)
        else:
            width, height = self.width, self.height
            cdll.DestroyMagickWand(self.__wand)
            self.__wand = blank(width, height, fill)._claim_wand()
    
    @only_live
    def set_alpha(self, alpha):
        """Set alpha channel of pixels in the image.
        
           :param alpha: target alpha value
           :type alpha: float
           
           Resets alpha channel of all pixels in the image to given
           value between 0 (transpanret) and 1 (opaque).
           
           This method can be chained.
        """
        guard(self.__wand,
              lambda: cdll.MagickSetImageOpacity(self.__wand, alpha))
    
    @only_live
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
        if not composite:
            composite = composites.over
            
        value = enum_lookup(composite)
        
        guard(self.__wand,
              lambda: cdll.MagickCompositeImage(self.__wand, image.wand,
                                                value, x, y))
    
    @only_live
    def shadow(self, radius, x=0, y=0, opacity=0.5):
        guard(self.__wand,
              lambda: cdll.MagickShadowImage(self.__wand, opacity,
                                             radius, x, y))
    
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
        background = color.from_string('transparent')
            
        # preserve background color
        old_color = color.Color()
        guard(self.__wand,
              lambda: cdll.MagickGetImageBackgroundColor(self.__wand,
                                                         old_color.wand))
        guard(self.__wand,
              lambda: cdll.MagickSetImageBackgroundColor(self.__wand,
                                                         background.wand))
        
        guard(self.__wand,
              lambda: cdll.MagickSpliceImage(self.__wand, width,
                                             height, x, y))
        
        #restore background color
        guard(self.__wand,
              lambda: cdll.MagickSetImageBackgroundColor(self.__wand,
                                                         old_color.wand))
        old_color.close()
        background.close()
    
    @property
    @only_live
    def wand(self):
        """Return underlyimg ImageMagick resource.
           
           Useful when you want to perform custom operations directly
           accessing ctypes.
           :rtype: :class:`tinyimag.api.type.MagickWand_p`
        """
        return self.__wand
    
    def _claim_wand(self):
        """Reclaims wand from this image.
           
           :rtype: :class:`pystacia.api.type.MagickWand_p`
           
           For internal use only. Do not use directly. Reclaims wand of this
           image from owning by this object. Object is closed afterwards.
        """
        wand = self.__wand
        self.__wand = None
        self.close()
        
        return wand
    
    def colorspace():  # @NoSelf
        doc = (  # @UnusedVariable
        """Return or set colorspace associated with image.
           
           Sets or gets colorspace. When you set this property there's no
           colorspace conversion performed and the original channel values
           are just left as is. If you actually want to perform a conversion
           use :attr:`convert_colorspace` instead. Popular colorspace include
           RGB, YCbCr, grayscale and so on.
           
           :rtype: :class:`pystacia.lazyenum.EnumValue`
        """)
        
        @only_live
        def fget(self):
            value = cdll.MagickGetImageColorspace(self.__wand)
            return enum_reverse_lookup(colorspaces, value)
        
        @only_live
        def fset(self, mnemonic):
            value = enum_lookup(mnemonic)
            guard(self.__wand,
                  lambda: cdll.MagickSetImageColorspace(self.__wand, value))
        
        return property(**locals())
    
    colorspace = colorspace()
    
    def type():  # @ReservedAssignment @NoSelf
        doc = (  # @UnusedVariable
        """Set or get image type.
           
           :rtype: :class:`pystacia.lazyenum.EnumValue`
           
           Popular image types include truecolor, pallete, bilevel and their
           matter counterparts.
           
           >>> img = read('example.jpg')
           >>> img.type == types.truecolor
        """)
        
        @only_live
        def fget(self):
            value = cdll.MagickGetImageType(self.__wand)
            return enum_reverse_lookup(types, value)
        
        @only_live
        def fset(self, mnemonic):
            value = enum_lookup(mnemonic)
            guard(self.__wand,
                  lambda: cdll.MagickSetImageType(self.__wand, value))
            
        return property(**locals())
    
    type = type()  # @ReservedAssignment
    
    @only_live
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
           
        colorspace = enum_lookup(colorspace)
        guard(self.__wand,
              lambda: cdll.MagickTransformImageColorspace(self.__wand,
                                                          colorspace))
    
    @property
    @only_live
    def width(self):
        """Get image width.
           
           :rtype: ``int``
           
           Return image width in pixels.
        """
        return cdll.MagickGetImageWidth(self.__wand)
    
    @property
    @only_live
    def height(self):
        """Get image height.
           
           :rtype: ``int``
           
           Return image height in pixels.
        """
        return cdll.MagickGetImageHeight(self.__wand)
    
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
    
    def depth():  # @NoSelf
        doc = (  # @UnusedVariable
        """Set or get image depth per channel.
        
           :rtype: ``int``
           
           Set or get depth per channel in bits. Either 8 or 16.
        """)
        
        @only_live
        def fget(self):
            return cdll.MagickGetImageDepth(self.__wand)
        
        @only_live
        def fset(self, value):
            guard(self.__wand,
                  lambda: cdll.MagickSetImageDepth(self.__wand, value))
            
        return property(**locals())
    
    depth = depth()
    
    def show(self):
        """Display an image in GUI.
           
           :rtype: ``str``
           
           Saves image to temporary lossless file format on a disk and sends
           it to default image handling program to display. Returns a path
           to the temporary file. You get no gurantees about life span of a
           file since it will be typically deleted when image gets closed.
        """
        extension = 'bmp'
        delegates = magick.get_delegates()
        if 'png' in delegates:
            extension = 'png'
            
        tmpname = mkstemp()[1] + '.' + extension
        self.write(tmpname)
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

    @only_live
    def close(self):
        """Close image and free resources.
           
           Closes image freeing underlying :term:`ImageMagick` resources.
           After performing this operation image cant be used anymore
           and will throw exceptions.
           
           :rtype: ``type(None)``
        """
        if self.__wand:
            cdll.DestroyMagickWand(self.__wand)
            self.__wand = None
        
        self.__closed = True
    
    @property
    def closed(self):
        """Check if image is closed.
           
           Returns ``True`` if image has been closed and cannot be
           used anymore. ``False`` otherwise.
           
           :rtype: ``bool``
        """
        return self.__closed
    
    def __del__(self):
        if not self.__closed:
            self.close()
    
    def __repr__(self):
        template = '<{class_}(w={w},h={h},{depth}bit'\
                   ',{colorspace},{type}) object at {addr}>'
        w, h = self.size
        depth, type = self.depth, self.type.name  # @ReservedAssignment
        colorspace, addr = self.colorspace.name, hex(addressof(self.__wand[0]))
        class_ = self.__class__.__name__
        
        return formattable(template).format(class_=class_, w=w, h=h,
                                            depth=depth, colorspace=colorspace,
                                            addr=addr, type=type)

import webbrowser
from tempfile import mkstemp
from ctypes import c_size_t, byref, string_at, addressof
from os import environ
from os.path import exists
from math import atan, degrees

from six import b

from pystacia.compat import formattable
from pystacia import color
color_module = color
from pystacia.util import TinyException
from pystacia.api.func import guard
from pystacia import magick
from pystacia import cdll, enum_lookup, enum_reverse_lookup, _register_cleanup
from pystacia.lazyenum import enum

if not 'fftw' in magick.get_delegates():
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

types = enum('type')
filters = enum('filter')
colorspaces = enum('colorspace')
compressions = enum('compression')
composites = enum('composite')
axes = enum('axis')
