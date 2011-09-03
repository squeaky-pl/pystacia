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

class Image(object):
    def __init__(self, wand=None):
        if not wand:
            pass
        
        self.__wand = wand
        self.__closed = False
    
    @classmethod
    def read(cls, filename, file=None):
        wand = cdll.NewMagickWand()
        
        return cls.__init__(wand=wand)
    
    @only_live
    def close(self):
        cdll.DestroyMagickWand(self.__wand)
        self.__closed = True
    
    @property
    def closed(self): return self.__closed
    
    def __del__(self):
        if not self.__closed: self.close()

init()

__all__ = [Image]