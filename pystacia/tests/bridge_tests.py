from pystacia.tests.common import TestCase
from pystacia.bridge import SimpleImpl, ThreadImpl


class BridgeTest(TestCase):
    impls = [ThreadImpl, SimpleImpl]
    
    def test_one(self):
        for impl in self.__class__.impls:
            bridge = Bridge(lambda x: 2 * x, impl())
            
            self.assertEquals(bridge.request(2), 4)
            self.assertEquals(bridge.request(3), 6)
            self.assertEquals(bridge.request(0), 0)
            
            bridge.shutdown()
        
    def test_many(self):
        for impl in self.__class__.impls:
            bridge = Bridge(lambda x: x + 2, impl())
            
            def thread():
                for _ in range(randint(0, 20)):
                    i = randint(0, 100)
                    self.assertEquals(bridge.request(i), i + 2)
            
            threads = [Thread(target=thread) for _ in range(randint(0, 100))]
            [t.start() for t in threads]
            [t.join() for t in threads]
            
            bridge.shutdown()
    
    def test_call(self):
        for impl in self.__class__.impls:
            bridge = CallBridge(impl())
            
            self.assertEquals(bridge.call(lambda: 0), 0)
            self.assertEquals(bridge.call(lambda x: x - 2, 2), 0)
            self.assertEquals(bridge.call(lambda x, y: x * y, 2, 3), 6)
            
            def kw(one, two):
                return one + 2 * two
            
            self.assertEquals(bridge.call(kw, one=1, two=2), 5)
            
            bridge.shutdown()


from pystacia.bridge import Bridge, CallBridge

from threading import Thread
from random import randint
