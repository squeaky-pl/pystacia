from unittest import TestCase


class Enum(TestCase):
    def test(self):
        composite = enum('composite')
        
        self.assertEquals(composite.name, 'composite')
        self.assertEquals(composite.atop.name, 'atop')
        
        #test memoized
        self.assertEquals(enum('qwerty'), enum('qwerty'))
        
        self.assertEquals(composite.qwerty, composite.qwerty)
        self.assertEquals(id(composite.qwerty), id(composite.qwerty))
        
        self.assertNotEqual(composite.qwerty, composite.abc)


from tinyimg.lazyenum import enum
