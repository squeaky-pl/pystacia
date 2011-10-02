from unittest import TestCase

from tinyimg.enums import lookup
from tinyimg.lazyenum import enum

composite = enum('composite')

class EnumTestCase(TestCase):
    def test(self):
        self.assertEquals(lookup(composite.non_existant, (6, 6)), None)
        
        self.assertEquals(lookup(composite.undefined, (6, 6, 2, 10)), 0)
        
        self.assertEquals(lookup(composite.undefined, (2, 6, 2, 10)), None)
        
        self.assertEquals(lookup(composite.undefined, (6, 7, 2, 8)), 0)
        
        self.assertEquals(lookup(composite.darken_intensity, (6, 7, 2, 1)), 66)