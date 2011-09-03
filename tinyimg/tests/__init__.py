from os.path import join, dirname
from unittest import TestCase, skip

from .. import Image, TinyException, read


images = join(dirname(__file__), '../../images')

class CloseTestCase(TestCase):
    @skip('not implemented')
    def test(self):
        img = Image()
        self.assertEquals(img.closed, False)
        
        img.close()
        self.assertEquals(img.closed, True)
        
        self.assertRaises(TinyException, lambda: img.close())
        
        img.close()
        
class ReadTestCase(TestCase):
    def test(self):
        self.assertRaises(TinyException, lambda: read('/non/existant.jpg'))
        
class SizeTestCase(TestCase):
    def test(self):
        img = read(join(images, 'lena.bmp'))
        self.assertSequenceEqual(img.size, (512, 512))
        self.assertSequenceEqual((img.width, img.height), img.size)
        
        img.close()
        
class ResizeTestCase(TestCase):
    def test(self):
        img = read(join(images, 'lena.bmp'))
        img.resize(256, 256)
        
        self.assertSequenceEqual(img.size, (256, 256))
        
        img.resize(factor=.5)
        
        self.assertSequenceEqual(img.size, (128, 128))
        
        img.resize(factor=(1, .5))
        
        self.assertSequenceEqual(img.size, (128, 64))
        
        self.assertRaises(TinyException, lambda: img.resize())