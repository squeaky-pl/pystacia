from __future__ import division


def read_raw(raw, format, width, height, depth):  # @ReservedAssignment
    if hasattr(raw, 'read'):
        length = width * height * depth // 8
        raw = raw.read(length)
    
    format = b(format.upper())  # @ReservedAssignment
    
    wand = cdll.NewMagickWand()
    
    guard(wand, lambda: cdll.MagickSetSize(wand, width, height))
    guard(wand, lambda: cdll.MagickSetDepth(wand, depth))
    guard(wand, lambda: cdll.MagickSetFormat(wand, format))
        
    guard(wand, lambda: cdll.MagickReadImageBlob(wand, raw, len(raw)))
    
    return Image(wand)


def read_blob(blob, format, length=None):  # @ReservedAssignment
    if hasattr(blob, 'read'):
        blob = blob.read(length)
    
    wand = cdll.NewMagickWand()
    
    # ensure we always get bytes
    format = b(format.upper())  # @ReservedAssignment
    old_format = cdll.MagickGetImageFormat(wand)
    template = formattable('Format "{0}" unsupported')
    guard(wand,
          lambda: cdll.MagickSetFormat(wand, format),
          template.format(format))
    
    guard(wand, lambda: cdll.MagickReadImageBlob(wand, blob, len(blob)))
    
    guard(wand,
              lambda: cdll.MagickSetFormat(wand, old_format))
    
    return Image(wand)


def read(filename):
    wand = cdll.NewMagickWand()
        
    if not exists(filename):
        template = formattable('No such file or directory: {0}')
        raise IOError((2, template.format(filename)))
    
    filename = b(filename)
    
    guard(wand, lambda: cdll.MagickReadImage(wand, filename))
    
    return Image(wand)


def read_special(spec, width=None, height=None, _ctype=False):
    wand = cdll.NewMagickWand()
    
    if width and height:
        guard(wand, lambda: cdll.MagickSetSize(wand, width, height))
    
    spec = b(spec)
    
    guard(wand, lambda: cdll.MagickReadImage(wand, spec))
    
    return wand if _ctype else Image(wand)


def blank(width, height, background=None, _ctype=False):
    if not background:
        background = 'transparent'
    
    return read_special('xc:' + str(background), width, height, _ctype)

from tinyimg.util import only_live


class Image(object):
    def __init__(self, wand):
        self.__wand = wand
        self.__closed = not bool(wand)
    
    @only_live
    def copy(self):
        wand = cdll.CloneMagickWand(self.__wand)
        return self.__class__(wand)
    
    @only_live
    def write(self, filename):
        guard(self.__wand,
              lambda: cdll.MagickWriteImage(self.__wand, b(filename)))
        
    @only_live
    def get_blob(self, format):  # @ReservedAssignment
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
        
        return blob
        
    def get_raw(self, format):  # @ReservedAssignment
        return dict(raw=self.get_blob(format),
                    format=format,
                    width=self.width,
                    height=self.height,
                    depth=self.depth)
        
    @only_live
    def resize(self, width=None, height=None,
               factor=None, filter=None, blur=1):  # @ReservedAssignment
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
    
    @only_live
    def crop(self, width, height, x=0, y=0):
        guard(self.__wand,
              lambda: cdll.MagickCropImage(self.__wand, width, height, x, y))
    
    @only_live
    def rotate(self, angle):
        guard(self.__wand,
              lambda: cdll.MagickRotateImage(self.__wand,
                                             color.transparent.wand, angle))
    
    @only_live
    def set_alpha(self, alpha):
        guard(self.__wand,
              lambda: cdll.MagickSetImageOpacity(self.__wand, alpha))
    
    @only_live
    def fill(self, fill):
        if hasattr(cdll, 'MagickSetImageColor'):
            guard(self.__wand,
                  lambda: cdll.MagickSetImageColor(self.__wand, fill.wand))
        else:
            width, height = self.width, self.height
            cdll.DestroyMagickWand(self.__wand)
            self.__wand = blank(width, height, fill, _ctype=True)
    
    @only_live
    def flip(self, axis):
        if axis.name == 'x':
            guard(self.__wand, lambda: cdll.MagickFlipImage(self.__wand))
        elif axis.name == 'y':
            guard(self.__wand, lambda: cdll.MagickFlopImage(self.__wand))
        else:
            raise TinyException('axis must be X or Y')
        
    @only_live
    def roll(self, x, y):
        guard(self.__wand, lambda: cdll.MagickRollImage(self.__wand, x, y))
        
    @only_live
    def despeckle(self):
        guard(self.__wand, lambda: cdll.MagickDespeckleImage(self.__wand))
        
    @only_live
    def emboss(self, radius=0, sigma=0):
        guard(self.__wand,
              lambda: cdll.MagickEmbossImage(self.__wand, radius, sigma))
    
    @only_live
    def enhance(self):
        guard(self.__wand, lambda: cdll.MagickEnhanceImage(self.__wand))
    
    @only_live
    def equalize(self):
        guard(self.__wand, lambda: cdll.MagickEqualizeImage(self.__wand))
        
    @only_live
    def dft(self, magnitude):
        magnitude = bool(magnitude)
        guard(self.__wand,
              lambda: cdll.MagickForwardFourierTransformImage(self.__wand,
                                                              magnitude))
    
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
    def modulate(self, hue=100, saturation=100, lightness=100):
        guard(self.__wand,
              lambda: cdll.MagickModulateImage(self.__wand, lightness,
                                               saturation, hue))
    
    def desaturate(self):
        self.modulate(saturation=0)
        
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
    def sketch(self, sigma, radius=0, angle=45):
        guard(self.__wand,
              lambda: cdll.MagickSketchImage(self.__wand, radius,
                                             sigma, angle))
    
    #TODO fit mode
    @only_live
    def merge(self, other, x=0, y=0, composite=None):
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
    def sepia(self, threshold):
        guard(self.__wand,
              lambda: cdll.MagickSepiaToneImage(self.__wand, threshold))
    
    @only_live
    def overlay_color(self, color, blend=1):
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
                                            addr=addr)


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

composite = enum('composite')
image_type = enum('type')
image_filter = enum('filter')
colorspace = enum('colorspace')
compressions = enum('compression')
axes = enum('axis')
