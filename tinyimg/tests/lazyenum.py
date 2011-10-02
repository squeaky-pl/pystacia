from unittest import TestCase

from tinyimg.lazyenum import enum

class EnumTestCase(TestCase):
    def test(self):
        composite = enum('composite')
        
        self.assertEqual(composite.name, 'composite')
        self.assertEqual(composite.atop.name, 'atop')