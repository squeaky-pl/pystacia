from __future__ import with_statement

"""A many to one thread bridge"""


class Impl(object):
    def ___worker(): #@NoSelf
        def fget(self):
            if not self.__worker:
                raise PystaciaException('Worker not set')
            
            return self.__worker
        
        def fset(self, worker):
            self.__worker = worker
        
        return property(**locals())
    
    worker = ___worker()


class SimpleImpl(Impl):
    def lazy_start(self):
        pass
    
    def request(self, request):
        return self.worker(request)
    
    def shutdown(self):
        pass


class ThreadImpl(Impl):
    def __init__(self, daemon=False):
        self.__worker = None
        self.__loop = None
        self.__queue = None
        self.__lock = Lock()
        self.__daemon = daemon
        
    def lazy_start(self):
        if not self.__loop:
            with self.__lock:
                if not self.__loop:
                    self.__queue = queue.Queue()
                    self.__loop = ThreadLoop(self.__queue, self.worker)
                    if self.__daemon:
                        self.__loop.daemon = True
                    self.__loop.start()
    
    def request(self, request):
        # prevent from deadlocking on nested calls
        if self.loop == current_thread():
            response = self.worker(request)
        else:
            event = Event()
            event.request = request
            self.__queue.put(event)
            event.wait()
            response = event.response
        
        if isinstance(response, PassException):
            exc_info = response.exc_info
            reraise(*exc_info)
        
        return response
    
    def shutdown(self):
        """Shutdown bridge loop"""
        self.queue.put(Shutdown())
        self.loop.join()
        
        self.__loop = None
        self.__queue = None
    
    @property
    def queue(self):
        """Get an event queue"""
        if not self.__queue:
            raise PystaciaException('Loop not started')
        
        return self.__queue
    
    @property
    def loop(self):
        if not self.__loop:
            raise PystaciaException('Loop not started')
        
        return self.__loop

from threading import Thread, Event


class ThreadLoop(Thread):
    def __init__(self, queue, worker):
        self.__queue = queue
        self.__worker = worker
        
        super(ThreadLoop, self).__init__()
        
    def run(self):
        logger.debug('Starting loop thread')
        
        while 1:
            event = self.__queue.get()
            
            if isinstance(event, Shutdown):
                logger.debug('Received Shutdown message')
                break
            
            request = event.request
            
            try:
                response = self.__worker(request)
            except:
                logger.debug('Passing exception from loop')
                response = PassException()
            
            event.response = response
            event.set()
        
        logger.debug('Exiting loop thread')


class Bridge(object):
    def __init__(self, worker, impl=None):
        if not impl:
            impl = ThreadImpl(self)
        impl.worker = worker
        self.__impl = impl
        
    def request(self, request):
        """Send a request to a worker function.
           
           For requests coming from many threads it is guaranteed that they
           will be handled all in one the same separate thread in a sequential
           manner.
        """
        impl = self.__impl
        impl.lazy_start()
        return impl.request(request)
        
    def shutdown(self):
        self.__impl.shutdown()


class Shutdown():
    pass


class PassException():
    def __init__(self):
        from sys import exc_info
        self.exc_info = exc_info()


class CallBridge(Bridge):
    
    """A bridge that calls functions"""
    
    @staticmethod
    def __worker(request):
        callable_, args, kw = request
        return callable_(*args, **kw)
    
    def __init__(self, impl=None):
        super(CallBridge, self).__init__(self.__worker, impl)
        
    def call(self, callable_, *args, **kw):
        return self.request((callable_, args, kw))


from six import moves, reraise
queue = moves.queue
from time import sleep
from threading import Lock

try:
    from threading import current_thread
except ImportError:
    from threading import currentThread as current_thread

try:
    from thread import get_ident
except ImportError:
    from _thread import get_ident
    
from pystacia import logger
from pystacia.util import PystaciaException
