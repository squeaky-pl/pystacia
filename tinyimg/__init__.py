from __future__ import with_statement

import webbrowser
from sys import argv
from os.path import dirname, join, exists
import atexit
from tempfile import mkstemp
from ctypes import CDLL, c_size_t, byref, string_at
from ctypes.util import find_library

from .types import Filter
from tinyimg.utils import TinyException, only_live
from tinyimg.compat import BZ2File, formattable

from tinyimg.lazyenum import enum

composite = enum('composite')
image_type = enum('type')
colorspace = enum('colorspace')

def init():
    def try_overrides():
        paths = []
        
        from os import environ
        
        try: path = environ['VIRTUAL_ENV']
        except KeyError: pass
        else: paths.append(join(path, 'lib'))
        
        if not paths: return None
        
        import platform
        
        platform_dll_name = None
        if getattr(platform, 'mac_ver'):
            def platform_dll_name(v):
                return formattable('lib{0}.dylib').format(v)
        
        if not platform_dll_name: return None
        
        for path in paths:
            path = join(path, platform_dll_name('MagickWand'))
            if exists(path):
                return path
        
        return None
    
    # first let's look in some places that may override system-wide paths
    resolved_path = try_overrides()
    
    # still nothing? let ctypes figure it out
    if not resolved_path:
        resolved_path = find_library('MagickWand')
        
    if not resolved_path:
        raise TinyException('Could not find or load magickWand')
    
    global cdll
    cdll = CDLL(resolved_path)
    
    from .func import annote
    annote(cdll)
    
    cdll.MagickWandGenesis()
    atexit.register(lambda: cdll.MagickWandTerminus())

def read(filename=None, file=None):
    return Image.read(filename, file)

__lena_blob = None
def lena_blob():
    global __lena_blob
    
    if not __lena_blob:
        with BZ2File(join(dirname(__file__), 'lena.ycbcr.bz2')) as f:
            __lena_blob = dict(blob=f.read(), format='ycbcr', height=512, width=512, depth=8)
            
    return __lena_blob

def lena(size=None, colorspace=colorspace.rgb):
    img = Image(**lena_blob())
    if size: img.resize(size, size)
    if img.colorspace != colorspace:
        img.convert_colorspace(colorspace)
        
    return img

def get_magick_version_str():
    return cdll.MagickGetVersion(None)

__magick_version = None
def get_magick_version():
    global __magick_version
    
    if not __magick_version:
        options = get_magick_options()
        
        try: version = options['LIB_VERSION_NUMBER']
        except KeyError:
            try: version = options['VERSION']
            except KeyError: pass
            else: __magick_version = tuple(int(x) for x in version.split('.'))
        else: __magick_version = tuple(int(x) for x in version.split(','))
        
    return __magick_version

__magick_options = {}
def get_magick_options():
    global __magick_options
    
    if not __magick_options:
        size = c_size_t()
        keys = cdll.MagickQueryConfigureOptions(b('*'), size)
        for key in (keys[i] for i in range(size.value)):
            __magick_options[decode_char_p(key)] =\
            decode_char_p(cdll.MagickQueryConfigureOption(key))
            
    return __magick_options

import tinyimg.api.enum as enum_api

def enum_lookup(mnemonic, throw=True):
    value = enum_api.lookup(mnemonic, get_magick_version())
    if throw and value == None:
        template = formattable("Enumeration '{enum}' cant map mnemonic '{mnemonic}'")
        raise TinyException(template.format(enum=mnemonic.enum.name, mnemonic=mnemonic.name))
    return value

def enum_reverse_lookup(enum, value):
    return enum_api.reverse_lookup(enum, value, get_magick_version())

class Image(object):
    def __init__(self, width=None, height=None, depth=None,
                 format=None, blob=None, wand=None, debug=False):
        self.__wand = wand if wand else cdll.NewMagickWand()
        
        self.debug = debug

        if blob:
            try: blob = blob.read()
            except AttributeError: pass
            if width and height:
                guard(self.__wand, lambda: cdll.MagickSetSize(self.__wand, width, height))
            if depth:
                guard(self.__wand, lambda: cdll.MagickSetDepth(self.__wand, depth))
            if format:
                # ensure we always get bytes
                format = b(format.upper())
                guard(self.__wand, lambda: cdll.MagickSetFormat(self.__wand, format))
            guard(self.__wand, lambda: cdll.MagickReadImageBlob(self.__wand, blob, len(blob)))
            
        self.__closed = False
        
        if not self.__wand:
            raise TinyException('Couldnt initialize image')
    
    @only_live
    def clone(self):
        wand = cdll.CloneMagickWand(self.__wand)
        return self.__class__(wand=wand)
    
    copy = clone
    
    @classmethod
    def read(cls, filename=None, file=None):
        wand = cdll.NewMagickWand()
        
        if file:
            return cls(blob=file)
        
        if filename:
            if not exists(filename):
                template = formattable('No such file or directory: {0}')
                raise IOError((2, template.format(filename)))
            guard(wand, lambda: cdll.MagickReadImage(wand, filename))
            return cls(wand=wand)
    
    @only_live
    def write(self, filename):
        guard(self.__wand, lambda: cdll.MagickWriteImage(self.__wand, filename))
        
    @only_live
    def get_blob(self, format=None):
        if format:
            # ensure we always get bytes
            format = b(format.upper())
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
        
    @only_live
    def resize(self, width=None, height=None, factor=None, filter=None, blur=1):
        if not filter: filter = 'undefined'
        
        if not width and not height:
            if not factor:
                raise TinyException('Either width, height or factor must be provided')
            
            width, height = self.size
            if not hasattr(factor, '__getitem__'): factor = (factor, factor)
            width, height = int(width * factor[0]), int(height * factor[1])
        
        filter = getattr(Filter, filter.upper())
        
        guard(self.__wand, lambda: cdll.MagickResizeImage(self.__wand, width, height, filter, blur))
    
    @only_live
    def crop(self, width, height, x=0, y=0):
        guard(self.__wand, lambda: cdll.MagickCropImage(self.__wand, width, height, x, y))
    
    #TODO: fit
    @only_live
    def rotate(self, angle):
        guard(self.__wand, lambda: cdll.MagickRotateImage(self.__wand, transparent.wand, angle))
    
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
    def eval(self, expression):
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
        guard(self.__wand, lambda: cdll.MagickShearImage(self.__wand, transparent.wand, x_angle, y_angle))
    
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
    def merge(self, other, x=0, y=0, op=composite.atop):
        value = enum_lookup(op)
        
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
    
    type = property(__get_type, __set_type)
    
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
        tmpname = mkstemp()[1] + '.bmp'
        self.write(tmpname)
        webbrowser.open('file://' + tmpname)
    
    @only_live
    def close(self):
        cdll.DestroyMagickWand(self.__wand)
        self.__wand = None
        self.__closed = True
    
    @property
    def closed(self): return self.__closed
    
    def __del__(self):
        if not self.__closed: self.close()

init()

from .func import guard
from tinyimg.color import from_string

transparent = from_string('transparent')

from six import b, PY3
if PY3: decode_char_p = lambda v: v.decode('utf-8')
else: decode_char_p = lambda v: v
__all__ = ["Image", "lena", "read"]
