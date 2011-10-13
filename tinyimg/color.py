from tinyimg.util import only_live


class Color(object):
    def __init__(self, wand=None):
        self.__wand = wand if wand else cdll.NewPixelWand()
        self.__closed = False
    
    def __get_red(self):
        return saturate(cdll.PixelGetRed(self.__wand))
    
    def __set_red(self, value):
        cdll.PixelSetRed(self.__wand, value)
        
    red = property(__get_red, __set_red)
    
    r = red
    
    def __get_green(self):
        return saturate(cdll.PixelGetGreen(self.__wand))
    
    def __set_green(self, value):
        cdll.PixelSetGreen(self.__wand, value)
    
    green = property(__get_green, __set_green)
    
    g = green
    
    def __get_blue(self):
        return saturate(cdll.PixelGetBlue(self.__wand))
    
    def __set_blue(self, value):
        cdll.PixelSetBlue(self.__wand, value)
    
    blue = property(__get_blue, __set_blue)

    b = blue
    
    def __get_alpha(self):
        return saturate(cdll.PixelGetAlpha(self.__wand))
    
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
        if self.alpha == 1:
            template = formattable('rgb({0},{1},{2})')
        else:
            template = formattable('rgba({0},{1},{2},{3})')
        
        rgb = tuple(int(x * 255) for x in self.get_rgb())
        
        return template.format(*(rgb + (self.alpha,)))
    
    @property
    @only_live
    def wand(self):
        return self.__wand
    
    @only_live
    def copy(self):
        wand = cdll.ClonePixelWand(self.__wand)
        return Color(wand)
    
    def __eq__(self, other):
        return self.get_rgba() == other.get_rgba()
    
    def __str__(self):
        return self.get_string()
    
    @only_live
    def __repr__(self):
        template = ('<{class_}(r={0},g={1},b={2},a={3})'
                    ' object at {addr}>')
        kw = dict(addr=hex(addressof(self.__wand[0])),
                  class_=self.__class__.__name__)
        
        return formattable(template).format(*self.get_rgba(), **kw)


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


def saturate(v):
    if v == 0:
        return 0
    elif v == 1:
        return 1
    else:
        return round(v, 4)


from ctypes import addressof

from six import b

from tinyimg import cdll
from tinyimg.api.func import guard
from tinyimg.compat import formattable

transparent = from_string('transparent')
