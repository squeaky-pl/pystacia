from unittest import TestCase


class MemoizedTestCase(TestCase):
    def test(self):
        class A(object):
            pass
        
        @memoized
        def producer(arg=None):
            """doc"""
            return A()
        
        self.assertEqual(producer(), producer())
        self.assertNotEqual(producer(), producer(1))
        self.assertEqual(producer.__name__, 'producer')
        self.assertEqual(producer.__doc__, 'doc')


from tinyimg.util import memoized
