from pystacia.tests.common import TestCase
from pystacia.bridge import SimpleImpl, ThreadImpl


class ImplTest(TestCase):
    def test(self):
        impl = Impl()
        self.assertRaisesRegexp(PystaciaException, 'not set',
                                lambda: impl.worker)
        self.worker = lambda: 2
        self.assertEqual(self.worker(), 2)
        
    def test_isolated(self):
        impl = IsolatedImpl()
        self.assertRaisesRegexp(PystaciaException, 'not started',
                                lambda: impl.queue)
        
        self.assertRaisesRegexp(PystaciaException, 'not started',
                                lambda: impl.loop)


class BridgeTest(TestCase):
    impls = [ThreadImpl, SimpleImpl]
    
    def test_default_impl(self):
        bridge = Bridge(lambda: None)
        self.assertIsInstance(bridge.impl, ThreadImpl)
    
    def test_one(self):
        for impl in self.__class__.impls:
            bridge = Bridge(lambda x: 2 * x, impl())
            
            self.assertEqual(bridge.request(2), 4)
            self.assertEqual(bridge.request(3), 6)
            self.assertEqual(bridge.request(0), 0)
            
            bridge.shutdown()
        
    def test_many(self):
        for impl in self.__class__.impls:
            bridge = Bridge(lambda x: x + 2, impl())
            
            def thread():
                for _ in range(randint(0, 20)):
                    i = randint(0, 100)
                    self.assertEqual(bridge.request(i), i + 2)
            
            threads = [Thread(target=thread) for _ in range(randint(0, 100))]
            [t.start() for t in threads]
            [t.join() for t in threads]
            
            bridge.shutdown()
    
    def test_call(self):
        for impl in self.__class__.impls:
            bridge = CallBridge(impl())
            
            self.assertEqual(bridge.call(lambda: 0), 0)
            self.assertEqual(bridge.call(lambda x: x - 2, 2), 0)
            self.assertEqual(bridge.call(lambda x, y: x * y, 2, 3), 6)
            
            def kw(one, two):
                return one + 2 * two
            
            self.assertEqual(bridge.call(kw, one=1, two=2), 5)
            
            bridge.shutdown()


from threading import Thread
from random import randint

from pystacia.bridge import Bridge, CallBridge, Impl, IsolatedImpl
from pystacia.util import PystaciaException
