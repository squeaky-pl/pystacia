from tinyimg.compat import TestCase


class CloseTest(TestCase):
    def test(self):
        white = color.from_string('white')
        self.assertEquals(white.closed, False)
        white.close()
        self.assertRaises(TinyException, lambda: white.close())
        self.assertEquals(white.closed, True)


class GetStringTest(TestCase):
    def test(self):
        blue = color.from_string('blue')
        self.assertEquals(blue.get_string(), 'rgb(0,0,255)')
        blue.alpha = 0
        self.assertEquals(blue.get_string(), 'rgba(0,0,255,0)')


class CopyStringTest(TestCase):
    def test(self):
        blue = color.from_string('white')
        blue_copy = blue.copy()
        
        self.assertNotEqual(blue.wand, blue_copy.wand)
        self.assertSequenceEqual(blue.get_rgba(), blue_copy.get_rgba())


class RgbColorTestCase(TestCase):
    def test(self):
        rgb = (1, 0, 0)
        red = color.from_rgb(*rgb)
        
        self.assertSequenceEqual((red.red, red.r), (1, 1))
        self.assertSequenceEqual((red.green, red.g), (0, 0))
        self.assertSequenceEqual((red.blue, red.b), (0, 0))
        self.assertEqual((red.alpha, red.a), (1, 1))
        
        self.assertSequenceEqual(red.get_rgb(), rgb)
        self.assertSequenceEqual(red.get_rgba(), rgb + (1,))
        
        red.g = 1
        self.assertEqual(red.g, 1)
        self.assertEqual(red.green, 1)
        
        red.set_rgba(0, 1, 1, 0)
        
        self.assertEqual(red.get_rgba(), (0, 1, 1, 0))


class StringColorTestCase(TestCase):
    def test(self):
        white = color.from_string('white')
        self.assertEqual(white.get_rgba(), (1, 1, 1, 1))
        red = color.from_string('red')
        self.assertEqual(red.get_rgba(), (1, 0, 0, 1))


from tinyimg import color
from tinyimg.util import TinyException
