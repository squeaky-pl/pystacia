from tinyimg.tests_compat import TestCase


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


def StringColorTestCase(TestCase):
    def test(self):
        white = color.from_string('white')
        self.assertEqual(white.get_rgba(), (1, 1, 1, 1))
        red = color.from_string('red')
        self.assertEqual(red.get_rgba(), (1, 0, 0, 1))


from tinyimg import color
