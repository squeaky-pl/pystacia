from unittest import TestCase


class Util(TestCase):
    def test_only_live(self):
        class A(object):
            @only_live  # @UndefinedVariable
            def func(self):
                pass
        
        a = A()
        a.closed = False
        
        a.func()
        
        a.closed = True
        self.assertRaises(TinyException, lambda: a.func())
    
    def test_memoized(self):
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


from tinyimg.util import memoized, only_live, TinyException
