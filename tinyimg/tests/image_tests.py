from tinyimg.compat import TestCase


class CloseTestCase(TestCase):
    def test(self):
        img = lena()
        self.assertEquals(img.closed, False)
        
        img.close()
        self.assertEquals(img.closed, True)
        
        self.assertRaises(TinyException, lambda: img.close())


class ReadAndGetRawTestCase(TestCase):
    def test(self):
        data = dict(raw=b('\xff\xff\xff'), format='rgb',
                    depth=8, width=1, height=1)
        img = read_raw(**data)
        
        self.assertSequenceEqual(img.size, (1, 1))
        self.assertEqual(img.depth, 8)
        self.assertEqual(img.get_blob('rgb'), data['raw'])
        self.assertDictEqual(img.get_raw('rgb'), data)


class ReadBlobTestCase(TestCase):
    def test(self):
        img = lena()
        bmp = img.get_blob('bmp')
        
        for i in (bmp, BytesIO(bmp)):
            img = read_blob(i, 'bmp')
            
            self.assertSequenceEqual(img.size, (512, 512))
            self.assertEquals(img.type, image_type.true_color)
            self.assertEquals(img.colorspace, colorspace.rgb)
            self.assertEquals(img.depth, 8)


class ReadTestCase(TestCase):
    def test(self):
        self.assertRaises(IOError, lambda: read('/non/existant.qwerty'))
        
        img = lena()
        
        tmpname = mkstemp()[1] + '.bmp'
        img.write(tmpname)
        
        img.close()
        
        img = read(tmpname)
        
        self.assertSequenceEqual(img.size, (512, 512))
        self.assertEquals(img.type, image_type.true_color)
        self.assertEquals(img.colorspace, colorspace.rgb)
        self.assertEquals(img.depth, 8)
            
        img.close()


class BlankTestCase(TestCase):
    def test(self):
        img = blank(10, 20)
        
        self.assertEquals(img.get_pixel(5, 5).alpha, 0)
        self.assertSequenceEqual(img.size, (10, 20))
        
        img.close()
        
        rgba = (1, 0, 0, 0.5)
        img = blank(30, 40, color.from_rgba(*rgba))
        self.assertSequenceEqual(img.size, (30, 40))
        self.assertSequenceEqual(img.get_pixel(10, 10).get_rgba(), rgba)

        img.close()


class CopyTestCase(TestCase):
    def test(self):
        img = lena()
        copy = img.copy()
        
        self.assertNotEquals(img.wand, copy.wand)
        self.assertSequenceEqual(img.size, copy.size)
        copy.resize(factor=(2, 0.5))
        self.assertNotEqual(img.size, copy.size)
        
        img.close()
        copy.close()


class WriteTestCase(TestCase):
    def test(self):
        img = lena()
        
        tmpname = mkstemp()[1] + '.bmp'
        img.write(tmpname)
        
        img.close()
        
        img = read(tmpname)
        self.assertSequenceEqual(img.size, (512, 512))
        self.assertEquals(img.colorspace, colorspace.rgb)
        self.assertEquals(img.type, image_type.true_color)
        img.close()


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


from tempfile import mkstemp

from six import b, BytesIO

from tinyimg.util import TinyException
from tinyimg.image import (read, read_raw, read_blob, image_type,
                           colorspace, blank)
from tinyimg import color
from tinyimg import lena
