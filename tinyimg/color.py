from tinyimg.util import only_live

class Color(object):
    def __init__(self, wand):
        self.__wand = wand
        self.__closed = not bool(wand)
        
    @only_live
    def close(self):
        cdll.DestroyPixelWand(self.__wand)
        self.__closed = True
        
    @property
    def closed(self):
        return self.__closed
    
    @only_live
    def get_string(self):
        return decode_char_p(cdll.PixelGetColorAsString(self.__wand))
    
    @property
    @only_live
    def wand(self):
        return self.__wand
    
    def __str__(self):
        return self.get_string()
    
    def __repr__(self):
        template = '<tinyimg.color.Color {string} object at {address}>'
        return formattable(template).format(string=str(self), address=hex(id(self)))

def from_string(value):
    #ensure we also get "bytes"
    value = b(value)
    wand = cdll.NewPixelWand()
    guard(wand, lambda: cdll.PixelSetColor(wand, value))
    
    return Color(wand)

from six import b

from tinyimg import cdll
from tinyimg.func import guard
from tinyimg.compat import decode_char_p, formattable

transparent = from_string('transparent')