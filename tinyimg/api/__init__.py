min_version = (6, 5, 9, 0)
name = 'MagickWand'
abis = (5, 4, 3, None)

def search_paths():
    paths = []
    
    from os import environ
    
    try: path = environ['TINYIMG_LIBRARY_PATH']
    except KeyError: pass
    else: paths.append(path)
    
    if not environ.get('TINYIMG_SKIP_VIRTUAL_ENV'):
        try: path = environ['VIRTUAL_ENV']
        except KeyError: pass
        else: paths.append(join(path, 'lib'))
    
    if not paths: return None
    
    import platform
    
    dll_template = None
    if getattr(platform, 'mac_ver'):
        def dll_template(abi):
            return 'lib{name}.{abi}.dylib' if abi else 'lib{name}.dylib'
    elif platform.system().lower() == 'linux':
        def dll_template(abi):
            return 'lib{name}.so.{abi}' if abi else 'lib{name}.so'
        
    if not dll_template: return None
    
    for path in paths:
        for abi in abis:
            template = formattable(dll_template(abi))
            path = join(path, template.format(name=name, abi=abi))
            if exists(path):
                try: CDLL(path)
                except: pass
                else: return path
    
    return None


from ctypes import CDLL
from os.path import join, exists

from tinyimg.compat import formattable