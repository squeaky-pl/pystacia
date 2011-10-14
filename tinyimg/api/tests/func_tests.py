from tinyimg.compat import TestCase


class Guard(TestCase):
    def test(self):
        img = lena()
        
        ccall = lambda: cdll.MagickSetFormat(img.wand, b('lolz'))
        self.assertRaises(TinyException, lambda: guard(img.wand, ccall))
        
        guard(img.wand, lambda: cdll.MagickSetFormat(img.wand, b('bmp')))
        
        img.close()


from six import b

from tinyimg import lena, cdll
from tinyimg.api.func import guard
from tinyimg.util import TinyException
