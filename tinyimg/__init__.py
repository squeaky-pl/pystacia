from __future__ import with_statement

def init():
    def try_overrides():
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
    
    # first let's look in some places that may override system-wide paths
    resolved_path = try_overrides()
    
    # still nothing? let ctypes figure it out
    if not resolved_path:
        resolved_path = find_library('MagickWand')
        
    if not resolved_path:
        raise TinyException('Could not find or load magickWand')
    
    global cdll
    cdll = CDLL(resolved_path)
    
    from .func import annote
    annote(cdll)
    
    cdll.MagickWandGenesis()
    
    atexit.register(lambda: cdll.MagickWandTerminus())
    
    # warn if unsupported
    from tinyimg import magick
    from tinyimg.api import min_version
    version = magick.get_version()
    if version < min_version:
        from warnings import warn
        template = formattable('Unsupported version of MagickWand {0}')
        warn(template.format(version))

from tinyimg.util import memoized

def __raw_lena():
    with BZ2File(join(dirname(__file__), 'lena.ycbcr.bz2')) as f:
        return dict(raw=f.read(), format='ycbcr', height=512, width=512, depth=8)

# weakref memoization to let garbage collector clear it when needed
__lena = None
def __lena_image():
    global __lena
    
    if not __lena:
        lena = read_raw(**__raw_lena())
        __lena = weakref.ref(lena)
    else:
        lena = __lena()
        if not lena:
            lena = read_raw(**__raw_lena())
            __lena = weakref.ref(lena)
    
    return lena.copy()
    
def lena(size=None, colorspace=None):
    img = __lena_image()
    
    if size: img.resize(size, size)
    if not colorspace: colorspace=globals()['colorspace'].rgb
    if img.colorspace != colorspace:
        img.convert_colorspace(colorspace)
        
    return img

def magick_logo():
    return read_special('logo:')

import tinyimg.api.enum as enum_api

def enum_lookup(mnemonic, throw=True):
    value = enum_api.lookup(mnemonic, magick.get_version())
    if throw and value == None:
        template = formattable("Enumeration '{enum}' cant map mnemonic '{mnemonic}'")
        raise TinyException(template.format(enum=mnemonic.enum.name, mnemonic=mnemonic.name))
    return value

def enum_reverse_lookup(enum, value):
    return enum_api.reverse_lookup(enum, value, magick.get_version())


cdll = None

import atexit
import weakref
from ctypes import CDLL
from os.path import dirname, join, exists
from ctypes.util import find_library

from tinyimg.compat import BZ2File, formattable
from tinyimg.util import TinyException

init()

from tinyimg import magick

from tinyimg import color
from tinyimg.image import read_special
from tinyimg.image import *
from tinyimg import image

__all__ = image.__all__ + ['lena', 'magick_logo', 'color']
