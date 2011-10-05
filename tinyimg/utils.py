class TinyException(Exception): pass

def only_live(f):
    def wrapper(obj, *args, **kw):
        if obj.closed:
            template = formattable('{0} already closed')
            raise TinyException(template.format(obj.__class__))
        
        return f(obj, *args, **kw)
        
    return wrapper

# adapted from http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, f):
        self.f = f
        self.cache = {}
        self.__doc__ = f.__doc__
        self.__name__ =  f.__name__
        
    def __call__(self, *args):
        try: return self.cache[args]
        except KeyError:
            value = self.f(*args)
            self.cache[args] = value
            return value

from tinyimg.compat import formattable
