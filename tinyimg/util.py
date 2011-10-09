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

def find_library(name, abis):
    paths = []
    
    from os import environ
    
    try: path = environ['TINYIMG_LIBRARY_PATH']
    except KeyError: pass
    else: paths.append(path)
    
    if not environ.get('TINYIMG_SKIP_VIRTUAL_ENV'):
        try: path = environ['VIRTUAL_ENV']
        except KeyError: pass
        else:
            paths.append(join(path, 'lib'))
            paths.append(join(path, 'dll'))
    
    from os import getcwd
    paths.append(getcwd())
    
    from sys import platform as sys_platform
    import platform
    from tinyimg.compat import dist

    from ctypes import CDLL
    dll_template = None
    factory = CDLL

    macos = hasattr(platform, 'mac_ver') and platform.mac_ver()[0]
    linux = dist and dist()[0]
    windows = hasattr(platform, 'win32_ver') and platform.win32_ver()[0]
    from sys import version_info
    # on windows with 2.5 win32_ver is empty
    if version_info[:2] == (2, 5):
        import os
        windows = os.name == 'nt'

    if macos:
        def dll_template(abi):
            return 'lib{name}.{abi}.dylib' if abi else 'lib{name}.dylib'
    elif linux:
        def dll_template(abi):
            return 'lib{name}.so.{abi}' if abi else 'lib{name}.so'
    elif windows:
        from ctypes import WinDLL
        factory = WinDLL
        def dll_template(abi):
            return 'lib{name}-{abi}.dll' if abi else 'lib{name}.dll'
    
    if not dll_template: return None
    
    if windows:
        old_path = environ['PATH']
        path_template = formattable('{path};{old_path}')
    
    for path in paths:
        if not exists(path): continue
        
        for abi in abis:
            template = formattable(dll_template(abi))
            dll_path = join(path, template.format(name=name, abi=abi)) 
            if exists(dll_path):
                if windows:
                    # windows doesnt store absolute locations in DLLs
                    # we need to append current path to environ
                    environ['PATH'] = path_template.format(path=path, old_path=old_path)
                try: factory(dll_path)
                except:
                    if windows:
                        # restore os path
                        environ['PATH'] = old_path
                else: return dll_path
    
    return None


from ctypes import CDLL
from os.path import join, exists

from tinyimg.compat import formattable
