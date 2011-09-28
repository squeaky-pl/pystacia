class TinyException(Exception): pass

def only_live(f):
    def wrapper(obj, *args, **kw):
        if obj.closed: raise TinyException('{0} already closed'.format(obj.__class__))
        
        return f(obj, *args, **kw)
        
    return wrapper