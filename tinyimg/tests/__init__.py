from unittest import TestCase

from .. import Image, TinyException

class CloseTestCase(TestCase):
    def test(self):
        img = Image()
        self.assertEquals(img.closed, False)
        
        img.close()
        self.assertEquals(img.closed, True)
        
        self.assertRaises(TinyException, lambda: img.close())