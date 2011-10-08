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
        else:
            paths.append(join(path, 'lib'))
            paths.append(join(path, 'dll'))
    
    from os import getcwd
    paths.append(getcwd())
    
    from platform import system

    from ctypes import CDLL
    dll_template = None
    factory = CDLL

    macos = system().lower() == 'darwin'
    linux = system().lower() == 'linux'
    windows = system().lower() == 'windows'

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
            #import pdb; pdb.set_trace() 
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
