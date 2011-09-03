from sys import argv
import atexit
from ctypes import CDLL
from ctypes.util import find_library

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
    def resize(self):
        pass
    
    @only_live
    def close(self):
        cdll.DestroyMagickWand(self.__wand)
        self.__closed = True
    
    @property
    def closed(self): return self.__closed
    
    def __del__(self):
        if not self.__closed: self.close()

init()

from .func import guard

__all__ = [Image]