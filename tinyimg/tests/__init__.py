from unittest import TestCase, skip

from .. import Image, TinyException, read

class CloseTestCase(TestCase):
    @skip('not implemented')
    def test(self):
        img = Image()
        self.assertEquals(img.closed, False)
        
        img.close()
        self.assertEquals(img.closed, True)
        
        self.assertRaises(TinyException, lambda: img.close())
        
        img.close()
        
class ReadTestCase(TestCase):
    def test(self):
        self.assertRaises(TinyException, lambda: read('/non/existant.jpg'))