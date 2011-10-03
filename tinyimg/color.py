from tinyimg.utils import only_live

class Color(object):
    def __init__(self, wand):
        self.__wand = wand
        self.__closed = False
        
    @only_live
    def close(self):
        cdll.DestroyPixelWand(self.__wand)
        self.__closed = True
        
    @property
    def closed(self):
        return self.__closed
    
    @property
    @only_live
    def wand(self):
        return self.__wand

def from_string(value):
    #ensure we also get "bytes"
    value = b(value)
    wand = cdll.NewPixelWand()
    guard(wand, lambda: cdll.PixelSetColor(wand, value))
    
    return Color(wand)

from six import b

from tinyimg import cdll
from tinyimg.func import guard