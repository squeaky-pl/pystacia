# coding: utf-8
# pystacia/tests/image_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.image import Image
from pystacia.tests.common import TestCase, skipIf


class WithFactory(TestCase):
    def test_instantiate(self):
        class Subclass(Image):
            pass
        
        self.assertIsInstance(blank(30, 30), Image)
        self.assertIsInstance(blank(30, 30, factory=Subclass), Subclass)
        
        registry.image_factory = Subclass
        self.assertIsInstance(blank(30, 30), Subclass)
        registry.image_factory = Image
        
    def test_raw(self):
        data = dict(raw=b('\xff\xff\xff'), format='rgb',
                    depth=8, width=1, height=1)
        img = read_raw(**data)
        
        self.assertEqual(img.size, (1, 1))
        self.assertEqual(img.depth, 8)
        self.assertEqual(img.get_blob('rgb'), data['raw'])
        self.assertDictEqual(img.get_raw('rgb'), data)
        self.assertEqual(img.get_pixel(0, 0), color.from_string('white'))
        
        data = dict(raw=BytesIO(b('\xff\xff\xff')), format='rgb',
                    depth=8, width=1, height=1)
        
        img2 = read_raw(**data)
        
        self.assertTrue(img.is_same(img2))
        
        img.close()
        img2.close()
        
    def test_blank(self):
        img = blank(10, 20)
        
        self.assertEqual(img.get_pixel(5, 5).alpha, 0)
        self.assertEqual(img.size, (10, 20))
        
        img.close()
        
        background = color.from_rgba(1, 0, 0, 0.5)
        img = blank(30, 40, background)
        self.assertEqual(img.size, (30, 40))
        self.assertEqual(img.get_pixel(10, 10), background)

        img.close()
        
    def test_get_pixel(self):
        img = blank(5, 5, color.from_string('red'))
        self.assertEqual(img.get_pixel(0, 0), color.from_string('red'))
        img.close()
        
        img = blank(5, 5, color.from_string('blue'))
        self.assertEqual(img.get_pixel(0, 1), color.from_string('blue'))
        img.close()
        
        img = blank(5, 5, color.from_string('white'))
        self.assertEqual(img.get_pixel(1, 1), color.from_string('white'))
        img.close()


class WithSample(TestCase):
    def setUp(self):
        self.img = sample()
        
    def tearDown(self):
        self.img.close()
        
    def test_read_blob(self):
        img = self.img
        
        bmp = img.get_blob('bmp')
        bmp2 = img.get_blob('bmp', factory=BytesIO)
        
        self.assertEqual(bmp, bmp2.read())
        
        for i in (bmp, BytesIO(bmp)):
            img = read_blob(i)
            
            self.assertEqual(img.size, sample.size)
            self.assertEqual(img.type, sample.type)
            self.assertEqual(img.colorspace, colorspaces.rgb)
            self.assertEqual(img.depth, 8)
    
    def test_read(self):
        self.assertRaises(IOError, lambda: read('/non/existant.qwerty'))
        
        img = self.img
        
        tmpname = mkstemp()[1] + '.bmp'
        img.write(tmpname)
        
        img = read(tmpname)
        
        self.assertSequenceEqual(img.size, sample.size)
        self.assertEqual(img.type, sample.type)
        self.assertEqual(img.colorspace, colorspaces.rgb)
        self.assertEqual(img.depth, 8)
            
        img.close()
    
    def test_write(self):
        img = self.img
        
        tmpname = mkstemp()[1] + '.bmp'
        img.write(tmpname)
        
        img = read(tmpname)
        self.assertEqual(img.size, sample.size)
        self.assertEqual(img.colorspace, colorspaces.rgb)
        self.assertEqual(img.type, sample.type)
        img.close()
    
    def test_rescale(self):
        img = self.img
        
        img.rescale(256, 256)
        self.assertEqual(img.size, (256, 256))
        img.rescale(factor=.5)
        self.assertEqual(img.size, (128, 128))
        
        img.rescale(factor=(1, .5))
        
        self.assertEqual(img.size, (128, 64))
        self.assertRaises(PystaciaException, lambda: img.rescale())
    
    def test_resize(self):
        img = self.img
        
        img.resize(128, 128)
        self.assertEqual(img.size, (128, 128))
        img.resize(64, 64, 64, 64)
        self.assertEqual(img.size, (64, 64))
    
    def test_rotate(self):
        img = self.img
        
        size = img.size
        img.rotate(30)
        self.assertGreater(img.size, size)
        self.assertEqual(img.get_pixel(5, 5).alpha, 0)
    
    def test_set_alpha(self):
        img = self.img
        
        img.set_alpha(0.5)
        self.assertEqual(img.get_pixel(32, 32).alpha, 0.5)
        img.set_alpha(0.7)
        self.assertEqual(img.get_pixel(5, 5).alpha, 0.7)
        img.set_alpha(0)
        self.assertEqual(img.get_pixel(10, 50).alpha, 0)
        img.set_alpha(1)
        self.assertEqual(img.get_pixel(64, 64).alpha, 1)

    def test_set_color(self):
        img = self.img
        
        red = color.from_string('red')
        img.set_color(red)
        self.assertEqual(img.get_pixel(32, 32), red)
        transparent = color.from_string('transparent')
        img.set_color(transparent)
        self.assertEqual(img.get_pixel(128, 128).alpha, 0)
    
    def test_flip(self):
        img = self.img
        
        before = img.get_pixel(10, 10)
        img.flip(axes.x)
        pix = img.get_pixel(10, img.height - 1 - 10)
        self.assertEqual(pix, before)
        img.flip(axes.y)
        pix = img.get_pixel(img.width - 1 - 10, img.height - 1 - 10)
        self.assertEqual(pix, before)
    
    def test_roll(self):
        img = self.img
        
        before = img.get_pixel(img.width - 1 - 10, 10)
        img.roll(20, 0)
        pix = img.get_pixel(9, 10)
        self.assertEqual(pix, before)
        img.roll(0, 20)
        pix = img.get_pixel(9, 30)
        self.assertEqual(pix, before)
        
    # only checks if it doesnt blow up
    def test_despeckle(self):
        img = self.img
        
        img.despeckle()
    
    # only check if it doesnt blow up
    def test_emboss(self):
        img = self.img
        
        img.emboss()
    
    # only check if it doesnt blow up
    def test_denoise(self):
        img = self.img
        
        img.denoise()
    
    # only check if it doesnt blow up
    def test_equalize(self):
        img = self.img
        
        img.equalize()
    
    # only check if it doesnt blow up
    @skipIf(not hasattr(Image, 'dft'), 'ImageMagick without FFTW delegate')
    def test_dft(self):
        img = self.img
        
        result = img.dft()
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], Image)
        self.assertIsInstance(result[1], Image)
        self.assertEqual(result[0].size, img.size)
    
    def test_transpose(self):
        img = self.img
        
        before = img.get_pixel(10, 0)
        img.transpose()
        self.assertEqual(img.get_pixel(0, 10), before)
    
    def test_transverse(self):
        img = self.img
        
        before = img.get_pixel(20, 40)
        img.transverse()
        pix = img.get_pixel(img.width - 1 - 40, img.height - 1 - 20)
        self.assertEqual(pix, before)
    
    def test_wave(self):
        img = self.img
        
        img.wave(10, 100)
        new_size = (sample.size[0], sample.size[1] + 20)
        self.assertEqual(img.size, new_size)
        self.assertEqual(img.get_pixel(25, 10).alpha, 0)
        self.assertEqual(img.get_pixel(128, 128).alpha, 1)
    
    # only test if it doesnt blow up
    def test_fx(self):
        img = self.img
        
        img.fx('1/2 * u')
    
    def test_gamma(self):
        img = self.img
        
        rgba = img.get_pixel(128, 128).get_rgba()
        img.gamma(1)
        pix = img.get_pixel(128, 128)
        self.assertEqual(pix.get_rgba(), rgba)
        img.gamma(2)
        pix = img.get_pixel(128, 128)
        self.assertGreaterEqual(pix.get_rgba(), rgba)
    
    # only test if it doesnt blow up
    def test_swirl(self):
        img = self.img
        
        img.swirl(90)
    
    # only test if it doesnt blow up
    def test_spread(self):
        img = self.img
        
        img.spread(5)
    
    # only test if it doest blow up
    def test_auto_gamma(self):
        img = self.img
        
        img.auto_gamma()
    
    # only test if it doesnt blow up
    def test_auto_level(self):
        img = self.img
        
        img.auto_level()
    
    def test_blur(self):
        img = self.img
        
        img.blur(3)
    
    def test_brightness_brighten(self):
        img = self.img
        
        coords = (40, 40)
        before = img.get_pixel(*coords)
        img.brightness(0)
        self.assertEqual(img.get_pixel(*coords), before)
        img.brightness(0.5)
        self.assertGreaterEqual(img.get_pixel(*coords).get_rgba(),
                           before.get_rgba())
    
    def test_brightness_darken(self):
        img = self.img
        
        coords = (40, 40)
        before = img.get_pixel(*coords)
        img.brightness(-0.5)
        self.assertLessEqual(img.get_pixel(*coords).get_rgba(),
                        before.get_rgba())
        img.brightness(-1)
        self.assertEqual(img.get_pixel(*coords), color.from_string('black'))
        img.brightness(1)
        self.assertEqual(img.get_pixel(*coords), color.from_string('white'))
    
    def test_contrast(self):
        img = self.img
        
        coords = (40, 40)
        before = img.get_pixel(*coords)
        img.contrast(0)
        self.assertEqual(img.get_pixel(*coords), before)
        img.contrast(-1)
        self.assertEqual(img.get_pixel(*coords), color.from_rgb(.5, .5, .5))
    
    def test_modulate(self):
        img = self.img
        
        coords = (40, 40)
        before = img.get_pixel(*coords)
        img.modulate()
        self.assertEqual(img.get_pixel(*coords), before)
        
        img.modulate(lightness=-1)
        self.assertEqual(img.get_pixel(*coords), color.from_string('black'))
    
    def test_desaturate(self):
        img = self.img
        
        img.desaturate()
        pix = img.get_pixel(40, 40)
        self.assertEqual(pix.r, pix.g)
        self.assertEqual(pix.g, pix.b)
    
    def test_colorize(self):
        img = self.img
        
        red = color.from_string('red')
        
        img.colorize('red')
        
        self.assertEquals(img.get_pixel(50, 50).get_hsl()[0], red.get_hsl()[0])
    
    def test_invert(self):
        img = self.img
        
        coords = (40, 40)
        before = img.get_pixel(*coords).get_rgb()
        img.invert()
        after = img.get_pixel(*coords).get_rgb()
        self.assertEqual(tuple(x + y for x, y in zip(before, after)),
                         (1, 1, 1))
    
    # test if it doesnt blow
    def test_oil_paint(self):
        img = self.img
        
        img.oil_paint(3)
    
    def test_posterize(self):
        img = self.img
        
        img.posterize(4)
    
    def test_radial_blur(self):
        img = self.img
        
        coords = (256, 256)
        before = img.get_pixel(*coords)
        img.radial_blur(5)
        self.assertEqual(img.get_pixel(*coords), before)
    
    def test_skew(self):
        img = self.img
        
        width, height = img.size
        
        img.skew(5)
        self.assertTrue(img.get_pixel(2, 0).transparent)
        self.assertTrue(img.get_pixel(256, 256).opaque)
        self.assertEqual(img.width, width + 5)
        
        img.skew(5, axes.y)
        self.assertTrue(img.get_pixel(256, 1).transparent)
        self.assertTrue(img.get_pixel(256, 256).opaque)
        self.assertEqual(img.height, height + 5)

    def test_solarize(self):
        img = self.img
        
        before = img.get_pixel(256, 256)
        
        img.solarize(0)
        self.assertEqual(img.get_pixel(256, 256), before)
        img.solarize(1)
        self.assertEqual(img.get_pixel(256, 256).get_rgb(),
                          tuple(round(1 - x, 4) for x in before.get_rgb()))
    
    # test only if it doesnt blow up
    def test_normalize(self):
        img = self.img
        
        img.normalize()
        
    def test_threshold(self):
        img = self.img
        
        img.threshold()
        
        self.assertEqual(img.total_colors, 2)
    
    # test only if it doesnt blow up
    def test_map(self):
        img = self.img
        
        img.map(img)
        
    # test only if it doesnt blow up
    def test_contrast_stretch(self):
        img = self.img
        
        img.contrast_stretch()
        
    def test_total_colors(self):
        img = self.img
        
        img.type = 'bilevel'
        
        self.assertEqual(img.total_colors, 2)
    
    def test_motion_blur(self):
        img = self.img
        copy = img.copy()
        
        copy.motion_blur(5)
        self.assertFalse(img.is_same(copy))
    
    def test_adaptive_blur(self):
        img = self.img
        
        img.adaptive_blur(5)
    
    def test_adaptive_sharpen(self):
        img = self.img
        
        img.adaptive_sharpen(5)
    
    def test_detect_edges(self):
        img = self.img
        
        img.detect_edges(2)
    
    def test_sharpen(self):
        img = self.img
        
        img.sharpen(2)
        
    def test_add_noise(self):
        img = self.img
        copy = img.copy()
        
        copy.add_noise()
        self.assertFalse(img.is_same(copy))
    
    def test_charcoal(self):
        img = self.img
        copy = img.copy()
        
        copy.charcoal(2)
        
        self.assertFalse(img.is_same(copy))
    
    def test_shade(self):
        img = self.img
        copy = img.copy()
        
        copy.shade()
        
        self.assertTrue(copy.type, 'grayscale')
        self.assertFalse(img.is_same(copy))
    
    def test_get_range(self):
        img = self.img
        
        range = img.get_range()  # @ReservedAssignment
        
        self.assertNotEqual(range[0], range[1])
        
        img = blank(10, 10, 'white')
        
        self.assertEqual(range[0], range[1])
        self.assertEqual(range[0], 1)
    
    def test_evaluate(self):
        img = self.img
        img.type = 'grayscale'
        
        before = img.get_pixel(320, 240)
        
        img.evaluate('divide', 2)
        
        self.assertAlmostEqual(before.r, img.get_pixel(320, 240).r * 2, 2)
    
    # test only if it doesnt blow up
    def test_sketch(self):
        img = self.img
        
        img.sketch(2)
    
    def test_overlay(self):
        img = self.img
        
        img2 = img.copy()
        img2.rescale(50, 50)
        before = img2.get_pixel(10, 10)
        img.overlay(img2, 50, 50)
        self.assertEqual(img.get_pixel(60, 60), before)
    
    def test_compare(self):
        img = self.img
        
        result = img.compare(img)
        self.assertEqual(result[1], 0)
        self.assertIsInstance(result[0], Image)
        
        img2 = img.copy()
        
        result = img.compare(img2)
        self.assertEqual(result[1], 0)
        
        img2.gamma(2)
        
        result = img.compare(img2)
        self.assertNotEquals(result[1], 0)
        
        img2.close()
        
        img3 = img.copy().rescale(10, 10)
        
        self.assertFalse(img.compare(img3))
        
        img3.close()
        
    def test_is_same(self):
        img = self.img
        
        self.assertTrue(img.is_same(img))
        
        img2 = img.copy()
        
        self.assertTrue(img.is_same(img2))
        
        img2.gamma(2)
        
        self.assertFalse(img.is_same(img2))
        
        img2.close()
    
    def test_straigten(self):
        img = self.img
        
        img.rotate(5)
        size = img.size
        img.straighten(100)
        self.assertGreater(img.size, size)

    def test_sepia(self):
        img = self.img
        
        img.sepia()

    def test_fill(self):
        img = self.img
        
        red = color.from_string('red')
        img.fill(red)
        self.assertEqual(img.get_pixel(40, 40), red)

    def test_get_pixel_red(self):
        img = blank(5, 5, color.from_string('red'))
        self.assertEqual(img.get_pixel(0, 0), color.from_string('red'))
        img.close()
        
        img = blank(5, 5, color.from_string('blue'))
        self.assertEqual(img.get_pixel(0, 1), color.from_string('blue'))
        img.close()
        
        img = blank(5, 5, color.from_string('white'))
        self.assertEqual(img.get_pixel(1, 1), color.from_string('white'))
        img.close()
    
    def test_splice(self):
        img = self.img
        
        img.splice(10, 10, 10, 10)
        self.assertTrue(img.get_pixel(5, 5).opaque)
        self.assertEqual(img.get_pixel(15, 15).alpha, 0)
    
    def test_trim(self):
        img = self.img
        
        img.rotate(5)
        img.rotate(-5)
        size = img.size
        img.trim()
        self.assertLess(img.size, size)
    
    def test_colorspace(self):
        img = self.img
        
        self.assertEqual(img.colorspace, colorspaces.rgb)
        img.colorspace = colorspaces.ycbcr
        self.assertEqual(img.colorspace, colorspaces.ycbcr)
    
    def test_type(self):
        img = self.img
        
        self.assertEqual(img.type, sample.type)
        img.type = types.bilevel
        self.assertEqual(img.type, types.bilevel)
    
    def test_size(self):
        img = self.img
        
        self.assertSequenceEqual(img.size, sample.size)
        self.assertSequenceEqual((img.width, img.height), img.size)
    
    def test_depth(self):
        img = self.img
        
        self.assertEqual(img.depth, 8)
        img.depth = 16
        self.assertEqual(img.depth, 16)
        
    def test_convert_colorspace(self):
        img = self.img
        img.convert_colorspace(colorspaces.ycbcr)
        self.assertEqual(img.colorspace, colorspaces.ycbcr)
    
    def test_show(self):
        img = self.img
        
        tmpname = img.show(no_gui=True)
        
        if 'png' in magick.get_formats():
            self.assertTrue(tmpname.endswith('.png'))
        else:
            self.assertTrue(tmpname.endswith('.bmp'))
        
        self.assertTrue(read(tmpname).is_same(img))
    
    def test_checkerboard(self):
        img = self.img
        img2 = img.copy().checkerboard()
        
        checkerboard_ = checkerboard(*img.size)
        
        self.assertTrue(img.is_same(img2))
        
        blank_ = blank(*img.size).checkerboard()
        
        self.assertTrue(blank_.is_same(checkerboard_))
        
    def test_repr(self):
        img = self.img
        result = match('<Image\(w=(\d+),h=(\d+),(\d+)bit,(\w+),(\w+)\)',
                       repr(img))
        self.assertEqual(result.groups(),
                         tuple(str(x) for x in img.size + (img.depth,
                                                           img.colorspace.name,
                                                           img.type.name)))


class ThreadedTest(TestCase):
    def test(self):
        def thread():
            imgs = [blank(512, 512) for _ in range(randint(1, 10))]
            [i.close() for i in imgs]
            
        threads = [Thread(target=thread) for _ in range(10)]
        [t.start() for t in threads]
        [t.join() for t in threads]


from threading import Thread
from tempfile import mkstemp
from re import match

from six import b, BytesIO

from pystacia.util import PystaciaException
from pystacia.image import (read, read_raw, read_blob, types,
                           colorspaces, blank, axes, checkerboard)
from pystacia import color, magick, registry
from pystacia.tests.common import sample
from random import randint
