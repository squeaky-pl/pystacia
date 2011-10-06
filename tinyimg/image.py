from __future__ import division

def read_raw(raw, format, width, height, depth): #@ReservedAssignment
    if hasattr(raw, 'read'):
        length = width * height * depth // 8
        raw = raw.read(length)
    
    format = b(format.upper()) #@ReservedAssignment
    
    wand = cdll.NewMagickWand()
    
    guard(wand, lambda: cdll.MagickSetSize(wand, width, height))
    guard(wand, lambda: cdll.MagickSetDepth(wand, depth))
    guard(wand, lambda: cdll.MagickSetFormat(wand, format))
    
    guard(wand, lambda: cdll.MagickReadImageBlob(wand, raw, len(raw)))
    
    return Image(wand)

def read_blob(blob, length=None):
    if hasattr(blob, 'read'): blob = blob.read(length)
    
    wand = cdll.NewMagickWand()
    
    guard(wand, lambda: cdll.MagickReadImageBlob(wand, blob, len(blob)))
    
    return Image(wand)
    
def read(filename):
    wand = cdll.NewMagickWand()
        
    if not exists(filename):
        template = formattable('No such file or directory: {0}')
        raise IOError((2, template.format(filename)))
    
    filename = b(filename)
    
    guard(wand, lambda: cdll.MagickReadImage(wand, filename))
    
    return Image(wand)

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
        guard(self.__wand, lambda: cdll.MagickWriteImage(self.__wand, filename))
        
    @only_live
    def get_blob(self, format): #@ReservedAssignment
        if format:
            # ensure we always get bytes
            format = b(format.upper()) #@ReservedAssignment
            old_format = cdll.MagickGetImageFormat(self.__wand)
            template = formattable('Format "{0}" unsupported')
            guard(self.__wand,
                  lambda: cdll.MagickSetImageFormat(self.__wand, format),
                  template.format(format))
        
        size = c_size_t()
        result = guard(self.__wand, lambda: cdll.MagickGetImageBlob(self.__wand, byref(size)))
        blob = string_at(result, size.value)
        cdll.MagickRelinquishMemory(result)
        
        if format:
            guard(self.__wand, lambda: cdll.MagickSetImageFormat(self.__wand, old_format))
        
        return blob
        
    def get_raw(self, format): #@ReservedAssignment
        return dict(raw=self.get_blob(format),
                    format=format,
                    width=self.width,
                    height=self.height,
                    depth=self.depth)
        
    @only_live
    def resize(self, width=None, height=None, factor=None, filter=None, blur=1): #@ReservedAssignment
        if not filter:
            filter = image_filter.undefined #@ReservedAssignment
        
        if not width and not height:
            if not factor:
                raise TinyException('Either width, height or factor must be provided')
            
            width, height = self.size
            if not hasattr(factor, '__getitem__'): factor = (factor, factor)
            width, height = int(width * factor[0]), int(height * factor[1])
        
        value = enum_lookup(filter)
        
        guard(self.__wand, lambda: cdll.MagickResizeImage(self.__wand, width, height, value, blur))
    
    @only_live
    def crop(self, width, height, x=0, y=0):
        guard(self.__wand, lambda: cdll.MagickCropImage(self.__wand, width, height, x, y))
    
    #TODO: fit
    @only_live
    def rotate(self, angle):
        guard(self.__wand, lambda: cdll.MagickRotateImage(self.__wand, color.transparent.wand, angle))
    
    @only_live
    def set_opacity(self, opacity):
        guard(self.__wand, lambda: cdll.MagickSetImageOpacity(self.__wand, opacity))
    
    @only_live
    def flip(self, axis):
        if axis.upper() == 'X':
            guard(self.__wand, lambda: cdll.MagickFlipImage(self.__wand))
        elif axis.upper() == 'Y':
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
        guard(self.__wand, lambda: cdll.MagickEmbossImage(self.__wand, radius, sigma))
    
    @only_live
    def enhance(self):
        guard(self.__wand, lambda: cdll.MagickEnhanceImage(self.__wand))
    
    @only_live
    def equalize(self):
        guard(self.__wand, lambda: cdll.MagickEqualizeImage(self.__wand))
        
    @only_live
    def dft(self, magnitude):
        guard(self.__wand, lambda: cdll.MagickForwardFourierTransformImage(self.__wand, bool(magnitude)))
    
    @only_live
    def transpose(self):
        guard(self.__wand, lambda: cdll.MagickTransposeImage(self.__wand))
    
    @only_live
    def transverse(self):
        guard(self.__wand, lambda: cdll.MagickTransverseImage(self.__wand))
        
    @only_live
    def wave(self, amplitude, length):
        guard(self.__wand, lambda: cdll.MagickWaveImage(self.__wand, amplitude, length))
        
    @only_live
    def eval(self, expression): #@ReservedAssignment
        wand = guard(self.__wand, lambda: cdll.MagickFxImage(self.__wand, expression))
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
        guard(self.__wand, lambda: cdll.MagickAutoGammaImage(self.__wand))
    
    @only_live
    def auto_level(self):
        guard(self.__wand, lambda: cdll.MagickAutoLevelImage(self.__wand))
        
    @only_live
    def blur(self, radius=0, sigma=0):
        guard(self.__wand, lambda: cdll.MagickBlurImage(self.__wand, radius, sigma))
    
    @only_live
    def brightness(self, percent):
        guard(self.__wand, lambda: cdll.MagickBrightnessContrastImage(self.__wand, percent, 0))
    
    @only_live
    def modulate(self, hue=100, saturation=100, lightness=100):
        guard(self.__wand, lambda: cdll.MagickModulateImage(self.__wand, lightness, saturation, hue))
    
    def desaturate(self):
        self.modulate(saturation=0)
        
    @only_live
    def invert(self, only_gray=False):
        guard(self.__wand, lambda: cdll.MagickNegateImage(self.__wand, only_gray))
        
    @only_live
    def oil_paint(self, radius):
        guard(self.__wand, lambda: cdll.MagickOilPaintImage(self.__wand, radius))
    
    @only_live
    def posterize(self, levels):
        guard(self.__wand, lambda: cdll.MagickPosterizeImage(self.__wand, levels))
    
    @only_live
    #TODO: moving center here
    def radial_blur(self, radius):
        guard(self.__wand, lambda: cdll.MagickRadialBlurImage(self.__wand, radius))
    
    @only_live
    def shadow(self, radius, x=0, y=0, opacity=0.5):
        guard(self.__wand, lambda: cdll.MagickShadowImage(self.__wand, opacity, radius, x, y))
        
    @only_live
    def shear(self, x_angle, y_angle):
        guard(self.__wand, lambda: cdll.MagickShearImage(self.__wand, color.transparent.wand, x_angle, y_angle))
    
    @only_live
    def solarize(self, threshold):
        guard(self.__wand, lambda:cdll.MagickSolarizeImage(self.__wand, threshold))
    
    @only_live
    def contrast(self, percent):
        guard(self.__wand, lambda: cdll.MagickBrightnessContrastImage(self.__wand, 0, percent))
        
    @only_live
    def sketch(self, sigma, radius=0, angle=45):
        guard(self.__wand, lambda: cdll.MagickSketchImage(self.__wand, radius, sigma, angle))
    
    #TODO fit mode
    @only_live
    def merge(self, other, x=0, y=0, composite=None):
        if not composite:
            composite = globals()['composite'].atop
            
        value = enum_lookup(composite)
        
        guard(self.__wand, lambda: cdll.MagickCompositeImage(self.__wand, other.wand, value, x, y))
    
    @only_live
    def deskew(self, threshold):
        guard(self.__wand, lambda: cdll.MagickDeskewImage(self.__wand, threshold))
    
    @only_live
    def sepia(self, threshold):
        guard(self.__wand, lambda: cdll.MagickSepiaToneImage(self.__wand, threshold))
    
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
        guard(self.__wand, lambda: cdll.MagickSetImageColorspace(self.__wand, value))
    
    colorspace = property(__get_colorspace, __set_colorspace)
    
    @only_live
    def __get_type(self):
        value = cdll.MagickGetImageType(self.__wand)
        return enum_reverse_lookup(image_type, value)
    
    @only_live
    def __set_type(self, mnemonic):
        value = enum_lookup(mnemonic)
        guard(self.__wand, lambda: cdll.MagickSetImageType(self.__wand, value))
    
    type = property(__get_type, __set_type) #@ReservedAssignment
    
    @only_live
    def convert_colorspace(self, mnemonic):
        value = enum_lookup(mnemonic)
        guard(self.__wand, lambda: cdll.MagickTransformImageColorspace(self.__wand, value))
    
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
        guard(self.__wand, lambda: cdll.MagickSetImageDepth(self.__wand, value))
    
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
    def closed(self): return self.__closed
    
    def __del__(self):
        if not self.__closed: self.close()
    
    def __repr__(self):
        template = '<tinyimg.Image({width},{height},{depth},{colorspace},{type}) object at {address}>'
        width, height = self.size
        depth, type = self.depth, self.type.name #@ReservedAssignment
        colorspace, address = self.colorspace.name, hex(id(self))
        
        return formattable(template).format(**locals())

import webbrowser
from tempfile import mkstemp
from ctypes import c_size_t, byref, string_at
from os.path import exists

from six import b

from tinyimg.compat import formattable
from tinyimg import color
from tinyimg.util import TinyException
from tinyimg.func import guard
from tinyimg import magick
from tinyimg import cdll, enum_lookup, enum_reverse_lookup
from tinyimg.lazyenum import enum

composite = enum('composite')
image_type = enum('type')
image_filter = enum('filter')
colorspace = enum('colorspace')

__all__ = ['read_raw', 'read', 'read_blob',
           'Image',
           'composite', 'image_type', 'image_filter', 'colorspace']