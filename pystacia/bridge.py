from __future__ import with_statement

"""A many to one thread bridge"""

class Bridge(object):
    def __init__(self, worker, daemon=False):
        self.__queue = queue.Queue()
        self.__worker = worker
        self.__daemon = daemon
        self.__lock = Lock()
        self.__loop = None
        
    def request(self, request):
        """Send a request to a worker function.
           
           For requests coming from many threads it is guaranteed that they
           will be handled all in one the same separate thread in a sequential
           manner.
        """
        if not self.__loop:
            with self.__lock:
                if not self.__loop:
                    self.__loop = Loop(self, self.__worker)
                    if self.__daemon:
                        self.__loop.daemon = True
                    self.__loop.start()
        
        # prevent from deadlocking on nested calls
        if self.__loop == current_thread():
            response = self.__worker(request)
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
        self.__queue.put(Shutdown())
        self.__loop.join()
    
    @property
    def queue(self):
        """Get bus dictionary"""
        return self.__queue

from threading import Thread, Event


class Shutdown():
    pass


class PassException():
    def __init__(self):
        from sys import exc_info
        self.exc_info = exc_info()


class Loop(Thread):
    def __init__(self, bridge, worker):
        self.__bridge = bridge
        self.__worker = worker
        
        super(Loop, self).__init__()
        
    def run(self):
        bridge = self.__bridge
        logger.debug('Starting bridge loop thread')
        
        while 1:
            event = bridge.queue.get()
            
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
        
        logger.debug('Exiting bridge loop thread')

class CallBridge(Bridge):
    
    """A bridge that calls functions"""
    
    def __init__(self, daemon=False):
        def worker(request):
            callable_, args, kw = request
            return callable_(*args, **kw)
            
        super(CallBridge, self).__init__(worker, daemon)
        
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
