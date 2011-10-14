from unittest import TestCase


class Memoized(TestCase):
    def test(self):
        class A(object):
            pass
        
        @memoized
        def producer(arg=None):
            """doc"""
            return A()
        
        self.assertEquals(producer(), producer())
        self.assertNotEqual(producer(), producer(1))
        self.assertEquals(producer.__name__, 'producer')
        self.assertEquals(producer.__doc__, 'doc')


from tinyimg.util import memoized
