# coding: utf-8
# pystacia/tests/image_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.image import Image
from pystacia.compat import TestCase, skipIf


class Close(TestCase):
    def test(self):
        img = lena()
        self.assertEquals(img.closed, False)
        
        img.close()
        self.assertEquals(img.closed, True)
        
        self.assertRaises(TinyException, lambda: img.close())


class ReadAndGetRaw(TestCase):
    def test(self):
        data = dict(raw=b('\xff\xff\xff'), format='rgb',
                    depth=8, width=1, height=1)
        img = read_raw(**data)
        
        self.assertEquals(img.size, (1, 1))
        self.assertEquals(img.depth, 8)
        self.assertEquals(img.get_blob('rgb'), data['raw'])
        self.assertDictEqual(img.get_raw('rgb'), data)
        self.assertEquals(img.get_pixel(0, 0), color.from_string('white'))


class ReadBlob(TestCase):
    def test(self):
        img = lena()
        bmp = img.get_blob('bmp')
        
        for i in (bmp, BytesIO(bmp)):
            img = read_blob(i)
            
            self.assertEquals(img.size, (512, 512))
            self.assertEquals(img.type, types.truecolor)
            self.assertEquals(img.colorspace, colorspaces.rgb)
            self.assertEquals(img.depth, 8)


class Read(TestCase):
    def test(self):
        self.assertRaises(IOError, lambda: read('/non/existant.qwerty'))
        
        img = lena()
        
        tmpname = mkstemp()[1] + '.bmp'
        img.write(tmpname)
        
        img.close()
        
        img = read(tmpname)
        
        self.assertSequenceEqual(img.size, (512, 512))
        self.assertEquals(img.type, types.truecolor)
        self.assertEquals(img.colorspace, colorspaces.rgb)
        self.assertEquals(img.depth, 8)
            
        img.close()


class Blank(TestCase):
    def test(self):
        img = blank(10, 20)
        
        self.assertEquals(img.get_pixel(5, 5).alpha, 0)
        self.assertEquals(img.size, (10, 20))
        
        img.close()
        
        background = color.from_rgba(1, 0, 0, 0.5)
        img = blank(30, 40, background)
        self.assertEquals(img.size, (30, 40))
        self.assertEquals(img.get_pixel(10, 10), background)

        img.close()


class Copy(TestCase):
    def test(self):
        img = lena()
        copy = img.copy()
        
        self.assertNotEquals(img.wand, copy.wand)
        self.assertEquals(img.size, copy.size)
        copy.rescale(factor=(2, 0.5))
        self.assertNotEqual(img.size, copy.size)
        
        img.close()
        copy.close()


class Write(TestCase):
    def test(self):
        img = lena()
        
        tmpname = mkstemp()[1] + '.bmp'
        img.write(tmpname)
        
        img.close()
        
        img = read(tmpname)
        self.assertEquals(img.size, (512, 512))
        self.assertEquals(img.colorspace, colorspaces.rgb)
        self.assertEquals(img.type, types.truecolor)
        img.close()


class Rescale(TestCase):
    def test(self):
        img = lena()
        
        img.rescale(256, 256)
        self.assertEquals(img.size, (256, 256))
        img.rescale(factor=.5)
        self.assertEquals(img.size, (128, 128))
        
        img.rescale(factor=(1, .5))
        
        self.assertEquals(img.size, (128, 64))
        self.assertRaises(TinyException, lambda: img.rescale())
        
        img.close()


class Resize(TestCase):
    def test(self):
        img = lena()
        
        img.resize(128, 128)
        self.assertEquals(img.size, (128, 128))
        img.resize(64, 64, 64, 64)
        self.assertEquals(img.size, (64, 64))
        
        img.close()


class Rotate(TestCase):
    def test(self):
        img = lena()
        
        size = img.size
        img.rotate(30)
        self.assertGreater(img.size, size)
        self.assertEquals(img.get_pixel(5, 5).alpha, 0)
        
        img.close()


class SetAlpha(TestCase):
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


class SetColor(TestCase):
    def test(self):
        img = lena()
        
        red = color.from_string('red')
        img.set_color(red)
        self.assertEquals(img.get_pixel(32, 32), red)
        transparent = color.from_string('transparent')
        img.set_color(transparent)
        self.assertEquals(img.get_pixel(128, 128).alpha, 0)
        
        img.close()


class Flip(TestCase):
    def test(self):
        img = lena()
        
        before = img.get_pixel(10, 10)
        img.flip(axes.x)
        pix = img.get_pixel(10, img.height - 1 - 10)
        self.assertEquals(pix, before)
        img.flip(axes.y)
        pix = img.get_pixel(img.width - 1 - 10, img.height - 1 - 10)
        self.assertEquals(pix, before)
        
        img.close()


class Roll(TestCase):
    def test(self):
        img = lena()
        
        before = img.get_pixel(img.width - 1 - 10, 10)
        img.roll(20, 0)
        pix = img.get_pixel(9, 10)
        self.assertEquals(pix, before)
        img.roll(0, 20)
        pix = img.get_pixel(9, 30)
        self.assertEquals(pix, before)
        
        img.close()


# only checks if it doesnt blow up
class Despeckle(TestCase):
    def test(self):
        img = lena()
        
        img.despeckle()
        
        img.close()


# only check if it doesnt blow up
class Emboss(TestCase):
    def test(self):
        img = lena()
        
        img.emboss()
        
        img.close()


# only check if it doesnt blow up
class Denoise(TestCase):
    def test(self):
        img = lena()
        
        img.denoise()
        
        img.close()


# only check if it doesnt blow up
class Equalize(TestCase):
    def test(self):
        img = lena()
        
        img.equalize()
        
        img.close()


# only check if it doesnt blow up
class Dft(TestCase):
    @skipIf(not hasattr(Image, 'dft'), 'ImageMagick without FFTW delegate')
    def test(self):
        img = blank(40, 40, color.from_string('red'))
        
        result = img.dft()
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], Image)
        self.assertIsInstance(result[1], Image)
        self.assertEqual(result[0].size, img.size)
        
        img.close()


class Transpose(TestCase):
    def test(self):
        img = lena()
        
        before = img.get_pixel(10, 0)
        img.transpose()
        self.assertEquals(img.get_pixel(0, 10), before)
        
        img.close()


class Transverse(TestCase):
    def test(self):
        img = lena()
        
        before = img.get_pixel(20, 40)
        img.transverse()
        pix = img.get_pixel(img.width - 1 - 40, img.height - 1 - 20)
        self.assertEquals(pix, before)
        
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
        self.assertEquals(img.get_pixel(*coords), before)
        img.brightness(0.5)
        self.assertGreater(img.get_pixel(*coords).get_rgba(),
                           before.get_rgba())
        img.close()
        
        img = lena()
        img.brightness(-0.5)
        self.assertLess(img.get_pixel(*coords).get_rgba(),
                        before.get_rgba())
        img.brightness(-1)
        self.assertEquals(img.get_pixel(*coords), color.from_string('black'))
        img.brightness(1)
        self.assertEquals(img.get_pixel(*coords), color.from_string('white'))
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
        self.assertEquals(img.get_pixel(*coords), before)
        
        img.modulate(lightness=-1)
        self.assertEquals(img.get_pixel(*coords), color.from_string('black'))
        
        img.close()


class Desaturate(TestCase):
    def test(self):
        img = lena()
        
        img.desaturate()
        pix = img.get_pixel(40, 40)
        self.assertEquals(pix.r, pix.g)
        self.assertEquals(pix.g, pix.b)
        
        img.close()


class Invert(TestCase):
    def test(self):
        img = lena()
        
        coords = (40, 40)
        before = img.get_pixel(*coords).get_rgb()
        img.invert()
        after = img.get_pixel(*coords).get_rgb()
        self.assertEquals(tuple(x + y for x, y in zip(before, after)),
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


class Skew(TestCase):
    def test(self):
        img = lena()
        
        width, height = img.size
        
        img.skew(5)
        self.assertTrue(img.get_pixel(2, 0).transparent)
        self.assertTrue(img.get_pixel(256, 256).opaque)
        self.assertEquals(img.width, width + 5)
        
        img.skew(5, axes.y)
        self.assertTrue(img.get_pixel(256, 1).transparent)
        self.assertTrue(img.get_pixel(256, 256).opaque)
        self.assertEquals(img.height, height + 5)
        
        img.close()


class Solarize(TestCase):
    def test(self):
        img = lena()
        
        before = img.get_pixel(256, 256)
        
        img.solarize(0)
        self.assertEquals(img.get_pixel(256, 256), before)
        img.solarize(1)
        self.assertEquals(img.get_pixel(256, 256).get_rgb(),
                          tuple(round(1 - x, 4) for x in before.get_rgb()))
        
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
        img2.rescale(50, 50)
        before = img2.get_pixel(10, 10)
        img.overlay(img2, 50, 50)
        self.assertEquals(img.get_pixel(60, 60), before)


class Straighten(TestCase):
    def test(self):
        img = lena()
        
        img.rotate(5)
        size = img.size
        img.straighten(100)
        self.assertGreater(img.size, size)
        
        img.close()


class Sepia(TestCase):
    def test(self):
        img = lena()
        
        img.sepia()
        
        img.close()


class Fill(TestCase):
    def test(self):
        img = lena()
        
        red = color.from_string('red')
        img.fill(red)
        self.assertEquals(img.get_pixel(40, 40), red)
        
        img.close()


class GetPixel(TestCase):
    def test(self):
        img = blank(5, 5, color.from_string('red'))
        self.assertEquals(img.get_pixel(0, 0), color.from_string('red'))
        img.close()
        
        img = blank(5, 5, color.from_string('blue'))
        self.assertEquals(img.get_pixel(0, 1), color.from_string('blue'))
        img.close()
        
        img = blank(5, 5, color.from_string('white'))
        self.assertEquals(img.get_pixel(1, 1), color.from_string('white'))
        img.close()


class Splice(TestCase):
    def test(self):
        img = lena()
        
        img.splice(10, 10, 10, 10)
        self.assertTrue(img.get_pixel(5, 5).opaque)
        self.assertEquals(img.get_pixel(15, 15).alpha, 0)
        
        img.close()


class Trim(TestCase):
    def test(self):
        img = lena()
        
        img.rotate(5)
        img.rotate(-5)
        size = img.size
        img.trim()
        self.assertLess(img.size, size)
        
        img.close()


class Colorspace(TestCase):
    def test(self):
        img = lena()
        
        self.assertEquals(img.colorspace, colorspaces.rgb)
        img.colorspace = colorspaces.ycbcr
        self.assertEquals(img.colorspace, colorspaces.ycbcr)
        
        img.close()


class Type(TestCase):
    def test(self):
        img = lena()
        
        self.assertEquals(img.type, types.truecolor)
        img.type = types.bilevel
        self.assertEquals(img.type, types.bilevel)
        
        img.close()


class SizeTestCase(TestCase):
    def test(self):
        img = lena()
        self.assertSequenceEqual(img.size, (512, 512))
        self.assertSequenceEqual((img.width, img.height), img.size)
        
        img.close()


class DepthTestCase(TestCase):
    def test(self):
        img = lena()
        self.assertEquals(img.depth, 8)
        img.close()


from tempfile import mkstemp

from six import b, BytesIO

from pystacia.util import TinyException
from pystacia.image import (read, read_raw, read_blob, types,
                           colorspaces, blank, axes)
from pystacia import color
from pystacia import lena
