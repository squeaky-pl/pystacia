min_version = (6, 5, 9, 0)

def search_paths():
    paths = []
    
    from os import environ
    
    try: path = environ['TINYIMG_LIBRARY_PATH']
    except KeyError: pass
    else: paths.append(path)
    
    try: path = environ['VIRTUAL_ENV']
    except KeyError: pass
    else: paths.append(join(path, 'lib'))
    
    if not paths: return None
    
    import platform
    
    platform_dll_name = None
    if getattr(platform, 'mac_ver'):
        def platform_dll_name(v):
            return formattable('lib{0}.dylib').format(v)
    
    if not platform_dll_name: return None
    
    for path in paths:
        path = join(path, platform_dll_name('MagickWand'))
        if exists(path):
            return path
    
    return None


from os.path import join, exists

from tinyimg.compat import formattable