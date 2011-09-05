from os.path import join, dirname
from unittest import TestCase, skip

from .. import Image, TinyException, read, lena


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

class CropTestCase(TestCase):
    def test(self):
        img = read(join(images, 'lena.bmp'))
        
        img.crop(128, 128)
        
        self.assertSequenceEqual(img.size, (128, 128))
        
        img.crop(64, 64, 64, 64)
        
        self.assertSequenceEqual(img.size, (64, 64))

class CloneTestCase(TestCase):
    def test(self):
        img = read(join(images, 'lena.bmp'))
        copy = img.clone()
        
        self.assertSequenceEqual(img.size, copy.size)
        
        copy.resize(factor=(2, 0.5))
        
        self.assertNotEqual(img.size, copy.size)
        
class ConstructFromBlobTestCase(TestCase):
    def test(self):
        img = Image(blob='\xff\xff\xff', format='rgb', depth=8, width=1, height=1)
        
        self.assertSequenceEqual(img.size, (1,1))
        self.assertEqual(img.depth, 8)
        self.assertEqual(img.get_blob('rgb'), '\xff\xff\xff')
        
class LenaTestCase(TestCase):
    def test(self):
        img = lena()
        
        self.assertSequenceEqual(img.size, (512, 512))
        
        img.close()
        
        img = lena(32)
        
        self.assertSequenceEqual(img.size, (32, 32))
        
        img.close()