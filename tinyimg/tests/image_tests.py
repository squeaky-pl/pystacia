from tinyimg.compat import TestCase


class CloseTestCase(TestCase):
    def test(self):
        img = lena()
        self.assertEquals(img.closed, False)
        
        img.close()
        self.assertEquals(img.closed, True)
        
        self.assertRaises(TinyException, lambda: img.close())


class ReadTestCase(TestCase):
    def test(self):
        self.assertRaises(IOError, lambda: read('/non/existant.jpg'))


class SizeTestCase(TestCase):
    def test(self):
        img = lena()
        self.assertSequenceEqual(img.size, (512, 512))
        self.assertSequenceEqual((img.width, img.height), img.size)
        
        img.close()


class ResizeTestCase(TestCase):
    def test(self):
        img = lena()
        img.resize(256, 256)
        
        self.assertSequenceEqual(img.size, (256, 256))
        
        img.resize(factor=.5)
        
        self.assertSequenceEqual(img.size, (128, 128))
        
        img.resize(factor=(1, .5))
        
        self.assertSequenceEqual(img.size, (128, 64))
        
        self.assertRaises(TinyException, lambda: img.resize())


class CropTestCase(TestCase):
    def test(self):
        img = lena()
        
        img.crop(128, 128)
        
        self.assertSequenceEqual(img.size, (128, 128))
        
        img.crop(64, 64, 64, 64)
        
        self.assertSequenceEqual(img.size, (64, 64))


class CopyTestCase(TestCase):
    def test(self):
        img = lena()
        copy = img.copy()
        
        self.assertNotEquals(img.wand, copy.wand)
        
        self.assertSequenceEqual(img.size, copy.size)
        
        copy.resize(factor=(2, 0.5))
        
        self.assertNotEqual(img.size, copy.size)


class ReadAndGetRawTestCase(TestCase):
    def test(self):
        data = dict(raw=b('\xff\xff\xff'), format='rgb',
                    depth=8, width=1, height=1)
        img = read_raw(**data)
        
        self.assertSequenceEqual(img.size, (1, 1))
        self.assertEqual(img.depth, 8)
        self.assertEqual(img.get_blob('rgb'), data['raw'])
        self.assertDictEqual(img.get_raw('rgb'), data)


from six import b

from tinyimg.util import TinyException
from tinyimg.image import read, read_raw
from tinyimg import lena
