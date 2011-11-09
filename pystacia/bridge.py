from __future__ import with_statement

"""A many to one thread bridge"""

class Bridge(object):
    def __init__(self, worker, daemon=False):
        self.__requests = queue.Queue()
        self.__responses = queue.Queue()
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
            this = get_ident()
            self.__requests.put((this, request))
            while 1:
                responses = self.__responses
                data = responses.get()
                ident, response = data
                if ident != this:
                    responses.put(data)
                    sleep(0)  # yield control to another thread
                else:
                    break
        
        if isinstance(response, PassException):
            exc_info = response.exc_info
            raise exc_info[0], exc_info[1], exc_info[2]
        
        return response
    
    def shutdown(self):
        """Shutdown bridge loop"""
        self.__requests.put(Shutdown())
    
    @property
    def requests(self):
        """Get requests queue"""
        return self.__requests
    
    @property
    def responses(self):
        """Get responses queue"""
        return self.__responses

from threading import Thread


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
        while 1:
            data = bridge.requests.get()
            
            if isinstance(data, Shutdown):
                break
            
            ident, request = data
            
            try:
                response = self.__worker(request)
            except:
                response = PassException()
                
            bridge.responses.put((ident, response))


class CallBridge(Bridge):
    
    """A bridge that calls functions"""
    
    def __init__(self, daemon=False):
        def worker(request):
            callable_, args, kw = request
            return callable_(*args, **kw)
            
        super(CallBridge, self).__init__(worker, daemon)
        
    def call(self, callable_, *args, **kw):
        return self.request((callable_, args, kw))


import six
queue = six.moves.queue
from time import sleep
from threading import Lock, current_thread
try:
    from thread import get_ident
except ImportError:
    from _thread import get_ident