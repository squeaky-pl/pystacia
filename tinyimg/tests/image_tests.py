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
        self.assertEquals(img.get_pixel(128, 128).alpha, 1)
        
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
        img.gamma(2)
        pix = img.get_pixel(128, 128)
        self.assertGreater(pix.get_rgba(), rgba)
        
        img.close()


# only test if it doesnt blow up
class Swirl(TestCase):
    def test(self):
        img = lena()
        
        img.swirl(90)
        
        img.close()


# only test if it doesnt blow up
class Spread(TestCase):
    def test(self):
        img = lena()
        
        img.spread(5)
        
        img.close()


# only test if it doest blow up
class AutoGamma(TestCase):
    def test(self):
        img = lena()
        
        img.auto_gamma()
        
        img.close()


# only test if it doesnt blow up
class AutoLevel(TestCase):
    def test(self):
        img = lena()
        
        img.auto_level()
        
        img.close()


class Blur(TestCase):
    def test(self):
        img = lena()
        
        img.blur(3)
        
        img.close()


class Brighness(TestCase):
    def test(self):
        img = lena()
        
        coords = (40, 40)
        before = img.get_pixel(*coords)
        img.brightness(0)
        self.assertEqual(img.get_pixel(*coords), before)
        img.brightness(0.5)
        self.assertGreater(img.get_pixel(*coords).get_rgba(),
                           before.get_rgba())
        img.close()
        
        img = lena()
        img.brightness(-0.5)
        self.assertLess(img.get_pixel(*coords).get_rgba(),
                        before.get_rgba())
        img.brightness(-1)
        self.assertEqual(img.get_pixel(*coords), color.from_string('black'))
        img.brightness(1)
        self.assertEqual(img.get_pixel(*coords), color.from_string('white'))
        img.close()


class Contrast(TestCase):
    def test(self):
        img = lena()
        
        coords = (40, 40)
        before = img.get_pixel(*coords)
        img.contrast(0)
        self.assertEquals(img.get_pixel(*coords), before)
        img.contrast(-1)
        self.assertEquals(img.get_pixel(*coords), color.from_rgb(.5, .5, .5))
        
        img.close()


class Modulate(TestCase):
    def test(self):
        img = lena()
        
        coords = (40, 40)
        before = img.get_pixel(*coords)
        img.modulate()
        self.assertEqual(img.get_pixel(*coords), before)
        
        img.modulate(lightness=-1)
        self.assertEqual(img.get_pixel(*coords), color.from_string('black'))
        
        img.close()


class Desaturate(TestCase):
    def test(self):
        img = lena()
        
        img.desaturate()
        pix = img.get_pixel(40, 40)
        self.assertEqual(pix.r, pix.g)
        self.assertEqual(pix.g, pix.b)
        
        img.close()


class Invert(TestCase):
    def test(self):
        img = lena()
        
        coords = (40, 40)
        before = img.get_pixel(*coords).get_rgb()
        img.invert()
        after = img.get_pixel(*coords).get_rgb()
        self.assertEqual(tuple(x + y for x, y in zip(before, after)),
                         (1, 1, 1))


class OilPlaint(TestCase):
    def test(self):
        img = lena()
        
        img.oil_paint(3)
        
        img.close()


class Posterize(TestCase):
    def test(self):
        img = lena()
        
        img.posterize(4)
        
        img.close()


class RadialBlur(TestCase):
    def test(self):
        img = lena()
        
        coords = (256, 256)
        before = img.get_pixel(*coords)
        img.radial_blur(5)
        self.assertEquals(img.get_pixel(*coords), before)
        
        img.close()


class Shear(TestCase):
    def test(self):
        img = lena()
        
        img.shear(5, 0)
        self.assertEquals(img.get_pixel(5, 5).alpha, 0)
        self.assertTrue(img.get_pixel(256, 256).opaque)
        img.shear(0, 5)
        self.assertEquals(img.get_pixel(256, 2).alpha, 0)
        self.assertTrue(img.get_pixel(256, 256).opaque)
        
        img.close()


class Sketch(TestCase):
    def test(self):
        img = lena()
        
        img.sketch(2)
        
        img.close()


class Overlay(TestCase):
    def test(self):
        img = lena()
        img2 = img.copy()
        img2.resize(50, 50)
        before = img2.get_pixel(10, 10)
        img.overlay(img2, 50, 50)
        self.assertEqual(img.get_pixel(60, 60), before)


class Deskew(TestCase):
    def test(self):
        img = lena()
        
        img.rotate(5)
        size = img.size
        img.deskew(100)
        self.assertGreater(img.size, size)
        
        img.close()


class Sepia(TestCase):
    def test(self):
        img = lena()
        
        img.sepia()
        
        img.close()


class OverlayColor(TestCase):
    def test(self):
        img = lena()
        
        red = color.from_string('red')
        img.color_overlay(red)
        self.assertEquals(img.get_pixel(40, 40), red)
        
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
