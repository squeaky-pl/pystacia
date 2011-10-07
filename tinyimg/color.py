from tinyimg.util import only_live

class Color(object):
    def __init__(self, wand):
        self.__wand = wand
        self.__closed = not bool(wand)
    
    def __get_red(self):
        return cdll.PixelGetRed(self.__wand)
    
    def __set_red(self, value):
        cdll.PixelSetRed(self.__wand, value)
        
    red = property(__get_red, __set_red)
    
    r = red
    
    def __get_green(self):
        return cdll.PixelGetGreen(self.__wand)
    
    def __set_green(self, value):
        cdll.PixelSetGreen(self.__wand, value)
    
    green = property(__get_green, __set_green)
    
    g = green
    
    def __get_blue(self):
        return cdll.PixelGetBlue(self.__wand)
    
    def __set_blue(self, value):
        cdll.PixelSetBlue(self.__wand, value)
    
    blue = property(__get_blue, __set_blue)

    b = blue
    
    def __get_alpha(self):
        return cdll.PixelGetAlpha(self.__wand)
    
    def __set_alpha(self, value):
        cdll.PixelSetAlpha(self.__wand, value)
    
    alpha = property(__get_alpha, __set_alpha)
    
    a = alpha
    
    def get_rgb(self):
        return (self.r, self.g, self.b)
    
    def get_rgba(self):
        return self.get_rgb() + (self.a,)
    
    def set_rgb(self, r, g, b):
        self.r, self.g, self.b = r, g, b
        
    def set_rgba(self, r, g, b, a):
        self.set_rgb(r, g, b)
        self.a = a
    
    @only_live
    def close(self):
        cdll.DestroyPixelWand(self.__wand)
        self.__closed = True
        
    @property
    def closed(self):
        return self.__closed
    
    @only_live
    def get_string(self):
        return native_str(cdll.PixelGetColorAsString(self.__wand))
    
    @property
    @only_live
    def wand(self):
        return self.__wand
    
    def __str__(self):
        return self.get_string()
    
    def __repr__(self):
        template = '<tinyimg.color.Color rgba{rgba} object at {address}>'
        return formattable(template).format(rgba=self.get_rgba(), address=hex(id(self)))

def from_string(value):
    #ensure we also get "bytes"
    value = b(value)
    wand = cdll.NewPixelWand()
    guard(wand, lambda: cdll.PixelSetColor(wand, value))
    
    return Color(wand)

def from_rgb(r, g, b):
    wand = cdll.NewPixelWand()
    
    cdll.PixelSetRed(wand, r)
    cdll.PixelSetGreen(wand, g)
    cdll.PixelSetBlue(wand, b)
    
    return Color(wand)

def from_rgba(r, g, b, a):
    color = from_rgb(r, g, b)
    
    cdll.PixelSetAlpha(color.wand, a)
    
    return color

from six import b

from tinyimg import cdll
from tinyimg.func import guard
from tinyimg.compat import native_str, formattable

transparent = from_string('transparent')