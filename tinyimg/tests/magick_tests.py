from tinyimg.compat import TestCase


class Magick(TestCase):
    def test_options(self):
        self.assertIsInstance(get_options(), dict)
        
    def test_version(self):
        self.assertIsInstance(get_version(), (tuple, NoneType))
        
        
from tinyimg.magick import get_options, get_version
