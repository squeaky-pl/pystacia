from tinyimg.compat import TestCase


class MagickLogo(TestCase):
    def test(self):
        img = magick_logo()
        
        self.assertEquals(img.size, (640, 480))
        self.assertEquals(img.type, image_type.palette)


class Lena(TestCase):
    def test(self):
        img = lena()
        self.assertEquals(img.size, (512, 512))
        self.assertEquals(img.type, image_type.true_color)
        self.assertEquals(img.colorspace, colorspace.rgb)
        img.close()
        
        img = lena(32, colorspace=colorspace.ycbcr)
        self.assertEquals(img.size, (32, 32))
        self.assertEquals(img.colorspace, colorspace.ycbcr)
        img.close()


from tinyimg import magick_logo, lena
from tinyimg.image import image_type, colorspace
