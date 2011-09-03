import webbrowser
from sys import argv
import atexit
from tempfile import mkstemp
from ctypes import CDLL, c_size_t, byref
from ctypes.util import find_library
from collections import Sequence

from .types import Filter

def init():
    global cdll
    cdll = CDLL(find_library('magickWand'))
    
    if not cdll: raise TinyException('Could not find or load magickWand')
    
    from .func import annote
    annote(cdll)
    
    cdll.MagickWandGenesis()
    atexit.register(lambda: cdll.MagickWandTerminus())

class TinyException(Exception): pass

def only_live(f):
    def wrapper(image, *args, **kw):
        if image.closed: raise TinyException('Image already closed')
        
        return f(image, *args, **kw)
        
    return wrapper

def read(filename=None, file=None):
    return Image.read(filename, file)

class Image(object):
    def __init__(self, wand=None):
        if not wand:
            pass
        
        self.__wand = wand
        self.__closed = False
    
    def clone(self):
        wand = cdll.CloneMagickWand(self.__wand)
        return self.__class__(wand=wand)
    
    @classmethod
    def read(cls, filename=None, file=None):
        wand = cdll.NewMagickWand()
        
        if filename:
            guard(wand, lambda: cdll.MagickReadImage(wand, filename))
            
        return cls(wand=wand)
    
    @only_live
    def write(self, filename):
        guard(self.__wand, lambda: cdll.MagickWriteImage(self.__wand, filename))
        
    @only_live
    def resize(self, width=None, height=None, factor=None, filter=None, blur=1):
        if not filter: filter = 'undefined'
        
        if not width and not height:
            if not factor:
                raise TinyException('Either width, height or factor must be provided')
            
            width, height = self.size
            if not isinstance(factor, Sequence): factor = (factor, factor)
            width, height = int(width * factor[0]), int(height * factor[1])
        
        filter = getattr(Filter, filter.upper())
        
        guard(self.__wand, lambda: cdll.MagickResizeImage(self.__wand, width, height, filter, blur))
    
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

__all__ = [Image]