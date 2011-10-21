from tinyimg.compat import TestCase


class MagickLogo(TestCase):
    def test(self):
        img = magick_logo()
        
        self.assertEquals(img.size, (640, 480))
        self.assertEquals(img.type, types.palette)


class Lena(TestCase):
    def test(self):
        img = lena()
        self.assertEquals(img.size, (512, 512))
        self.assertEquals(img.type, types.truecolor)
        self.assertEquals(img.colorspace, colorspaces.rgb)
        img.close()
        
        img = lena(32)
        self.assertEquals(img.size, (32, 32))
        self.assertEquals(img.colorspace, colorspaces.rgb)
        img.close()


from tinyimg import magick_logo, lena
from tinyimg.image import types, colorspaces
