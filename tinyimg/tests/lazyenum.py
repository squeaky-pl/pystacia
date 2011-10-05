from unittest import TestCase

from tinyimg.lazyenum import enum

class EnumTestCase(TestCase):
    def test(self):
        composite = enum('composite')
        
        self.assertEqual(composite.name, 'composite')
        self.assertEqual(composite.atop.name, 'atop')
        
        #test memoized
        self.assertEqual(enum('qwerty'), enum('qwerty'))
        
        self.assertEqual(composite.qwerty, composite.qwerty)
        self.assertEqual(id(composite.qwerty), id(composite.qwerty))
        
        self.assertNotEqual(composite.qwerty, composite.abc)