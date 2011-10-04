class TinyException(Exception): pass

def only_live(f):
    def wrapper(obj, *args, **kw):
        if obj.closed:
            template = formattable('{0} already closed')
            raise TinyException(template.format(obj.__class__))
        
        return f(obj, *args, **kw)
        
    return wrapper

from tinyimg.compat import formattable