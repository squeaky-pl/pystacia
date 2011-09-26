from unittest import TestCase

from tinyimg.enums import get_value

class EnumTestCase(TestCase):
    def test(self):
        self.assertEquals(get_value('composite', 'non_existant', (6, 6)), None)
        
        self.assertEquals(get_value('composite', 'undefined', (6, 6, 2, 10)), 0)
        
        self.assertEquals(get_value('composite', 'undefined', (2, 6, 2, 10)), None)
        
        self.assertEquals(get_value('composite', 'undefined', (6, 7, 2, 8)), 0)
        
        self.assertEquals(get_value('composite', 'darken_intensity', (6, 7, 2, 1)), 66)