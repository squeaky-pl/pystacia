from __future__ import division

""":class:`Image` creation and management operations"""


def read(filename):
    """Read :class:`Image` from filename.
       
       :param filename: file name to read
       :type filename: ``str``
       :rtype: :class:`Image`
       
       Reads file, determines its format and return an :class:`Image`
       representing it.
       
       >>> read('example.jpg')
       <Image(w=512,h=512,8bit,rgb,truecolor) object at 0x10302ee00L>
    """
    wand = cdll.NewMagickWand()
        
    if not exists(filename):
        template = formattable('No such file or directory: {0}')
        raise IOError((2, template.format(filename)))
    
    filename = b(filename)
    
    guard(wand, lambda: cdll.MagickReadImage(wand, filename))
    
    return Image(wand)


def read_blob(blob, format=None, length=None):  # @ReservedAssignment
    """Read :class:`Image` from a blob string or stream with a header.
       
       :param blob: blob data string or stream
       :type blob: ``str`` (Python 2.x) / ``bytes`` (Python 3.x) or
         file-like object
       :param format: container format such as :term:`JPEG` or :term:`BMP`
       :type format: ``str``
       :param length: read maximum this bytes from stream
       :type length: ``int``
       :rtype: :class:`Image`
       
       Reads image from string or data stream that contains a valid file
       header i.e. it carries information on image dimensions, bit depth and
       compression. Data format is equivalent to e.g. :term:`JPEG` file
       read into string(Python 2.x)/bytes(PYthon 3.x) or file-like object.
       It is useful in cases when you have open file-like object but not the
       file itself in the filesystem. That often happens in web applications
       which map :term:`POST` data with file-like objects. Format and length
       are typically not used but can be a hint when the information cannot be
       guessed from the data itself.
       
       >>> with file('example.jpg') as f:
       >>>     img = read_blob(f)
       >>> img
       <Image(w=512,h=512,8bit,rgb,truecolor) object at 0x10302ee00L>
    """
    if hasattr(blob, 'read'):
        blob = blob.read(length)
    
    wand = cdll.NewMagickWand()
    
    if format:
        # ensure we always get bytes
        format = b(format.upper())  # @ReservedAssignment
        old_format = cdll.MagickGetImageFormat(wand)
        template = formattable('Format "{0}" unsupported')
        guard(wand,
              lambda: cdll.MagickSetFormat(wand, format),
              template.format(format))
    
    guard(wand, lambda: cdll.MagickReadImageBlob(wand, blob, len(blob)))
    
    if format:
        guard(wand,
                  lambda: cdll.MagickSetFormat(wand, old_format))
    
    return Image(wand)


def read_raw(raw, format, width, height, depth):  # @ReservedAssignment
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
       :rtype: :class:`Image`
       
       Reads image data from a raw string or stream containing data in format
       such as :term:`RGB` or :term:`YCbCr`. The contained image has
       dimensions of width and height pixels. Each channel is of depth bits.
    
       >>> img = read_raw(b'\xff\x00\x00', 'rgb', 1, 1, 8)
       >>> img.get_pixel(0, 0) == color.from_string('red')
       True
    """
    if hasattr(raw, 'read'):
        raw = raw.read()
    
    format = b(format.upper())  # @ReservedAssignment
    
    wand = cdll.NewMagickWand()
    
    guard(wand, lambda: cdll.MagickSetSize(wand, width, height))
    guard(wand, lambda: cdll.MagickSetDepth(wand, depth))
    guard(wand, lambda: cdll.MagickSetFormat(wand, format))
        
    guard(wand, lambda: cdll.MagickReadImageBlob(wand, raw, len(raw)))
    
    return Image(wand)


def read_special(spec, width=None, height=None, _ctype=False):
    """Read special :term:`ImageMagick` image resource"""
    wand = cdll.NewMagickWand()
    
    if width and height:
        guard(wand, lambda: cdll.MagickSetSize(wand, width, height))
    
    spec = b(spec)
    
    guard(wand, lambda: cdll.MagickReadImage(wand, spec))
    
    return wand if _ctype else Image(wand)


def blank(width, height, background=None, _ctype=False):
    """Create :class:`Image` with monolithic background
       
       :param width: Width in pixels
       :type width: ``int``
       :param height: Height in pixels
       :type height: ``int``
       :param background: background color, defaults to fully transparent
       :type background: :class:`tinyimg.Color`
       
       Creates blank image of given dimensions filled with background color.
       
       >>> blank(32, 32, color.from_string('red'))
       <Image(w=32,h=32,16bit,rgb,palette) object at 0x108006000L>
    """
    if not background:
        background = 'transparent'
    
    return read_special('xc:' + str(background), width, height, _ctype)

from tinyimg.util import only_live


class Image(object):
    def __init__(self, wand=None):
        self.__wand = wand
        self.__closed = not bool(wand)
    
    @only_live
    def copy(self):
        """Create new independent copy of an image"""
        wand = cdll.CloneMagickWand(self.__wand)
        
        return Image(wand)
    
    @only_live
    def write(self, filename, format=None, compression=None, quality=None):
        """Write an image to filesystem.
           
           :param filename: file name to write to.
           :type filename: ``str``
           :param format: file format
           :type format: ``str``
           :param compression: compression algorithm
           :type compression: :class:`tinyimg.lazyenum.EnumValue`
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
                 quality=None):
        """Return a blob representing an image
           
           :param format: format of the output such as :term:`JPEG`
           :type format: ``str``
           :param compression: compression supported by format
           :type compression: :class:`tinyimg.lazyenum.EnumValue`
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
        
        return blob
        
    def get_raw(self, format):  # @ReservedAssignment
        """Return ``dict`` representing raw image data.
           
           :param format: format of the output such as :term:`RGB`
           :type format:  ``str``
           :rtype: ``dict``
           
           Returns raw data ``dict`` consisting of raw, format, width, height
           and depth keys along their values.
        """
        return dict(raw=self.get_blob(format),
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
           :type filter: :class:`tinyimg.lazuenym.Enums`
           
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
            filter = image_filter.undefined  # @ReservedAssignment
        
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
        
        return self
    
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
        
        return self
    
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
        
        return self
    
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
        
        return self
    
    @only_live
    def fill(self, fill):
        """Fill whole image with one color.
        
           :param fill: desired fill color
           :type fill: :class:`tinyimg.color.Color`
           
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
        else:
            width, height = self.width, self.height
            cdll.DestroyMagickWand(self.__wand)
            self.__wand = blank(width, height, fill, _ctype=True)
            
        return self
    
    @only_live
    def flip(self, axis):
        """Flip an image along given axis.
           
           :param axis: X or Y axis
           :type axis: :class:`tinyimg.lazyenum.EnumValue`
           
           Flips (mirrors) an image along :attr:`axes.x` or :attr:`axes.y`.
           
           This method can be chained.
        """
        if axis.name == 'x':
            guard(self.__wand, lambda: cdll.MagickFlipImage(self.__wand))
        elif axis.name == 'y':
            guard(self.__wand, lambda: cdll.MagickFlopImage(self.__wand))
        else:
            raise TinyException('axis must be X or Y')
        
        return self
    
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
        
        return self
    
    @only_live
    def despeckle(self):
        """Attempt to remove speckle preserving edges.
           
           Resulting image almost solid color areas are smoothed preserving
           edges.
           
           This method can be chained.
        """
        guard(self.__wand, lambda: cdll.MagickDespeckleImage(self.__wand))
        
        return self
    
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
        
        return self
    
    @only_live
    def enhance(self):
        """Attempt to remove noise preserving edges.
        
           Applies a digital filter that improves the quality of a
           noisy image.
           
           This method can be chained.
        """
           
        guard(self.__wand, lambda: cdll.MagickEnhanceImage(self.__wand))
        
        return self
    
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
        
        return self
        
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
        
        first.overlay(copy, composite=composite.copy)
        
        guard(copy.wand, lambda: cdll.MagickNextImage(copy.wand))
        
        second.overlay(copy, composite=composite.copy)
        
        copy.close()
        
        return (first, second)
    
    @only_live
    def transpose(self):
        guard(self.__wand, lambda: cdll.MagickTransposeImage(self.__wand))
    
    @only_live
    def transverse(self):
        guard(self.__wand, lambda: cdll.MagickTransverseImage(self.__wand))
        
    @only_live
    def wave(self, amplitude, length):
        transparent = color.from_string('transparent')
        
        old_color = color.Color()
        guard(self.__wand,
              lambda: cdll.MagickGetImageBackgroundColor(self.__wand,
                                                         old_color.wand))
        guard(self.__wand,
              lambda: cdll.MagickSetImageBackgroundColor(self.__wand,
                                                         transparent.wand))
        
        guard(self.__wand,
              lambda: cdll.MagickWaveImage(self.__wand, amplitude, length))
        
        guard(self.__wand,
              lambda: cdll.MagickSetImageBackgroundColor(self.__wand,
                                                         old_color.wand))
        old_color.close()
        transparent.close()
        
    @only_live
    def fx(self, expression):  # @ReservedAssignment
        wand = guard(self.__wand,
                     lambda: cdll.MagickFxImage(self.__wand, b(expression)))
        cdll.DestroyMagickWand(self.__wand)
        self.__wand = wand
    
    @only_live
    def gamma(self, gamma):
        guard(self.__wand, lambda: cdll.MagickGammaImage(self.__wand, gamma))
    
    @only_live
    def swirl(self, degrees):
        guard(self.__wand, lambda: cdll.MagickSwirlImage(self.__wand, degrees))
        
    @only_live
    def spread(self, radius):
        guard(self.__wand, lambda: cdll.MagickSpreadImage(self.__wand, radius))
        
    @only_live
    def auto_gamma(self):
        guard(self.__wand,
              lambda: cdll.MagickAutoGammaImage(self.__wand))
    
    @only_live
    def auto_level(self):
        guard(self.__wand,
              lambda: cdll.MagickAutoLevelImage(self.__wand))
        
    @only_live
    def blur(self, radius, strength=None):
        if strength == None:
            strength = radius
            
        guard(self.__wand,
              lambda: cdll.MagickBlurImage(self.__wand, radius, strength))
    
    @only_live
    def brightness(self, factor):
        guard(self.__wand,
              lambda: cdll.MagickBrightnessContrastImage(self.__wand,
                                                         factor * 100, 0))
    
    @only_live
    def contrast(self, factor):
        guard(self.__wand,
              lambda: cdll.MagickBrightnessContrastImage(self.__wand,
                                                         0, factor * 100))
    
    @only_live
    def modulate(self, hue=0, saturation=0, lightness=0):
        guard(self.__wand,
              lambda: cdll.MagickModulateImage(self.__wand,
                                               lightness * 100 + 100,
                                               saturation * 100 + 100,
                                               hue * 100 + 100))
    
    def desaturate(self):
        self.modulate(saturation=-1)
        
    @only_live
    def invert(self, only_gray=False):
        guard(self.__wand,
              lambda: cdll.MagickNegateImage(self.__wand, only_gray))
        
    @only_live
    def oil_paint(self, radius):
        guard(self.__wand,
              lambda: cdll.MagickOilPaintImage(self.__wand, radius))
    
    @only_live
    def posterize(self, levels):
        guard(self.__wand,
              lambda: cdll.MagickPosterizeImage(self.__wand, levels))
    
    @only_live
    #TODO: moving center here
    def radial_blur(self, radius):
        guard(self.__wand,
              lambda: cdll.MagickRadialBlurImage(self.__wand, radius))
    
    @only_live
    def shadow(self, radius, x=0, y=0, opacity=0.5):
        guard(self.__wand,
              lambda: cdll.MagickShadowImage(self.__wand, opacity,
                                             radius, x, y))
    
    @only_live
    def shear(self, x_angle, y_angle):
        guard(self.__wand,
              lambda: cdll.MagickShearImage(self.__wand,
                                            color.transparent.wand,
                                            x_angle, y_angle))
    
    @only_live
    def solarize(self, threshold):
        guard(self.__wand,
              lambda: cdll.MagickSolarizeImage(self.__wand, threshold))
    
    @only_live
    def sketch(self, radius, angle=45, strength=None):
        if strength == None:
            strength = radius
        guard(self.__wand,
              lambda: cdll.MagickSketchImage(self.__wand, radius,
                                             strength, angle))
    
    @only_live
    def overlay(self, other, x=0, y=0, composite=None):
        if not composite:
            composite = globals()['composite'].over
            
        value = enum_lookup(composite)
        
        guard(self.__wand,
              lambda: cdll.MagickCompositeImage(self.__wand, other.wand,
                                                value, x, y))
    
    @only_live
    def deskew(self, threshold):
        guard(self.__wand,
              lambda: cdll.MagickDeskewImage(self.__wand, threshold))
    
    @only_live
    def sepia(self, saturation=-.4, threshold=.8):
        threshold = 2 ** int(magick.get_options()['QuantumDepth']) * threshold
        
        guard(self.__wand,
              lambda: cdll.MagickSepiaToneImage(self.__wand, threshold))
        
        self.modulate(saturation=saturation)
    
    @only_live
    def color_overlay(self, color, blend=1):
        # image magick ignores alpha setting of color
        # let's incorporate it into blend
        blend *= color.alpha
        
        blend = color_module.from_rgb(blend, blend, blend)
        
        guard(self.__wand,
              lambda: cdll.MagickColorizeImage(self.__wand, color.wand,
                                               blend.wand))
        
        blend.close()
    
    @only_live
    def get_pixel(self, x, y):
        color = color_module.Color()
        
        guard(self.__wand,
              lambda: cdll.MagickGetImagePixelColor(self.__wand, x, y,
                                                    color.wand))
        
        return color
    
    def splice(self, x, y, width, height):
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
    
    def trim(self, similarity=10, background=None):
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
              lambda: cdll.MagickTrimImage(self.__wand, similarity))
        
        #restore background color
        guard(self.__wand,
              lambda: cdll.MagickSetImageBackgroundColor(self.__wand,
                                                         old_color.wand))
        
        if background_free:
            background.close()
            
    @property
    @only_live
    def wand(self):
        return self.__wand
    
    @only_live
    def __get_colorspace(self):
        value = cdll.MagickGetImageColorspace(self.__wand)
        return enum_reverse_lookup(colorspace, value)
    
    @only_live
    def __set_colorspace(self, mnemonic):
        value = enum_lookup(mnemonic)
        guard(self.__wand,
              lambda: cdll.MagickSetImageColorspace(self.__wand, value))
    
    colorspace = property(__get_colorspace, __set_colorspace)
    
    @only_live
    def __get_type(self):
        value = cdll.MagickGetImageType(self.__wand)
        return enum_reverse_lookup(image_type, value)
    
    @only_live
    def __set_type(self, mnemonic):
        value = enum_lookup(mnemonic)
        guard(self.__wand,
              lambda: cdll.MagickSetImageType(self.__wand, value))
    
    type = property(__get_type, __set_type)  # @ReservedAssignment
    
    @only_live
    def convert_colorspace(self, mnemonic):
        value = enum_lookup(mnemonic)
        guard(self.__wand,
              lambda: cdll.MagickTransformImageColorspace(self.__wand, value))
    
    @property
    @only_live
    def width(self):
        return cdll.MagickGetImageWidth(self.__wand)
    
    @property
    @only_live
    def height(self):
        return cdll.MagickGetImageHeight(self.__wand)
    
    @property
    def size(self):
        return (self.width, self.height)
    
    @only_live
    def __get_depth(self):
        return cdll.MagickGetImageDepth(self.__wand)
    
    @only_live
    def __set_depth(self, value):
        guard(self.__wand,
              lambda: cdll.MagickSetImageDepth(self.__wand, value))
    
    depth = property(__get_depth, __set_depth)
    
    def show(self):
        extension = 'bmp'
        delegates = magick.get_options().get('DELEGATES', '').split()
        if 'png' in delegates:
            extension = 'png'
            
        tmpname = mkstemp()[1] + '.' + extension
        self.write(tmpname)
        webbrowser.open('file://' + tmpname)
        
        return tmpname
    
    @only_live
    def close(self):
        cdll.DestroyMagickWand(self.__wand)
        self.__wand = None
        self.__closed = True
    
    @property
    def closed(self):
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
from os.path import exists

from six import b

from tinyimg.compat import formattable
from tinyimg import color
color_module = color
from tinyimg.util import TinyException
from tinyimg.api.func import guard
from tinyimg import magick
from tinyimg import cdll, enum_lookup, enum_reverse_lookup
from tinyimg.lazyenum import enum

if not 'fftw' in magick.get_delegates():
    del Image.dft

composite = enum('composite')
image_type = enum('type')
image_filter = enum('filter')
colorspace = enum('colorspace')
compressions = enum('compression')
axes = enum('axis')
