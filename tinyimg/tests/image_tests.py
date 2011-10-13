from tinyimg.compat import TestCase, skip


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
        
        img.close()


class CropTestCase(TestCase):
    def test(self):
        img = lena()
        
        img.crop(128, 128)
        self.assertSequenceEqual(img.size, (128, 128))
        img.crop(64, 64, 64, 64)
        self.assertSequenceEqual(img.size, (64, 64))
        
        img.close()


class RotateTestCase(TestCase):
    def test(self):
        img = lena()
        
        size = img.size
        img.rotate(30)
        self.assertGreater(img.size, size)
        self.assertEquals(img.get_pixel(5, 5).alpha, 0)
        
        img.close()


class SetAlphaTestCase(TestCase):
    def test(self):
        img = lena()
        
        img.set_alpha(0.5)
        self.assertEquals(img.get_pixel(32, 32).alpha, 0.5)
        img.set_alpha(0.7)
        self.assertEquals(img.get_pixel(5, 5).alpha, 0.7)
        img.set_alpha(0)
        self.assertEquals(img.get_pixel(10, 50).alpha, 0)
        img.set_alpha(1)
        self.assertEquals(img.get_pixel(64, 64).alpha, 1)
        
        img.close()


class FillTestCase(TestCase):
    def test(self):
        img = lena()
        
        red = color.from_string('red')
        img.fill(red)
        self.assertSequenceEqual(img.get_pixel(32, 32).get_rgba(),
                                 (1, 0, 0, 1))
        transparent = color.from_string('transparent')
        img.fill(transparent)
        self.assertEquals(img.get_pixel(128, 128).alpha, 0)
        
        img.close()


class FlipTestCase(TestCase):
    def test(self):
        img = lena()
        
        rgba = img.get_pixel(10, 10).get_rgba()
        img.flip(axes.x)
        pix = img.get_pixel(10, img.height - 1 - 10)
        self.assertSequenceEqual(pix.get_rgba(), rgba)
        img.flip(axes.y)
        pix = img.get_pixel(img.width - 1 - 10, img.height - 1 - 10)
        self.assertSequenceEqual(pix.get_rgba(), rgba)
        
        img.close()


class RollTestCase(TestCase):
    def test(self):
        img = lena()
        
        rgba = img.get_pixel(img.width - 1 - 10, 10).get_rgba()
        img.roll(20, 0)
        pix = img.get_pixel(9, 10)
        self.assertSequenceEqual(pix.get_rgba(), rgba)
        img.roll(0, 20)
        pix = img.get_pixel(10, 9)
        
        img.close()


# only checks if it doesnt blow up
class DespeckleTestCase(TestCase):
    def test(self):
        img = lena()
        
        img.despeckle()
        
        img.close()


# only check if it doesnt blow up
class EmbossTestCase(TestCase):
    def test(self):
        img = lena()
        
        img.emboss()
        
        img.close()


# only check if it doesnt blow up
class EnhanceTestCase(TestCase):
    def test(self):
        img = lena()
        
        img.enhance()
        
        img.close()

# only check if it doesnt blow up
class EqualizeTestCase(TestCase):
    def test(self):
        img = lena()
        
        img.equalize()
        
        img.close()


# only check if it doesnt blow up
class DftTestCase(TestCase):
    @skip
    def test(self):
        img = lena()
        
        img.dft()
        
        img.close()


class Transpose(TestCase):
    def test(self):
        img = lena()
        
        rgba = img.get_pixel(10, 0).get_rgba()
        img.transpose()
        self.assertEquals(img.get_pixel(0, 10).get_rgba(), rgba)
        
        img.close()


class Transverse(TestCase):
    def test(self):
        img = lena()
        
        rgba = img.get_pixel(20, 40).get_rgba()
        img.transverse()
        pix = img.get_pixel(img.width - 1 - 40, img.height - 1 - 20)
        self.assertSequenceEqual(pix.get_rgba(), rgba)
        
        img.close()


class Wave(TestCase):
    def test(self):
        img = lena()
        
        img.wave(10, 100)
        self.assertEquals(img.size, (512, 512 + 20))
        self.assertEquals(img.get_pixel(25, 10).alpha, 0)
        self.assertEquals(img.get_pixel(128 ,128).alpha, 1)
        
        img.close()


# only test if it doesnt blow up
class Fx(TestCase):
    def test(self):
        img = lena()
        
        img.fx('0')
        
        img.close()


class Gamma(TestCase):
    def test(self):
        img = lena()
        
        rgba = img.get_pixel(128, 128).get_rgba()
        img.gamma(1)
        pix = img.get_pixel(128, 128)
        self.assertEquals(pix.get_rgba(), rgba)
        
        img.close()


class SizeTestCase(TestCase):
    def test(self):
        img = lena()
        self.assertSequenceEqual(img.size, (512, 512))
        self.assertSequenceEqual((img.width, img.height), img.size)
        
        img.close()


from tempfile import mkstemp

from six import b, BytesIO

from tinyimg.util import TinyException
from tinyimg.image import (read, read_raw, read_blob, image_type,
                           colorspace, blank, axes)
from tinyimg import color
from tinyimg import lena
