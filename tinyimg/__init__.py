def init():
    from tinyimg.util import find_library
    from tinyimg.api import name, abis
    # first let's look in some places that may override system-wide paths
    resolved_path = find_library(name, abis)
    # still nothing? let ctypes figure it out
    if not resolved_path:
        from ctypes.util import find_library  # @Reimport
        resolved_path = find_library('MagickWand')
    if not resolved_path:
        raise TinyException('Could not find or load magickWand')
    
    from ctypes import CDLL
    factory = CDLL
    global cdll
    cdll = factory(resolved_path)
    from .func import annote
    annote(cdll)
    cdll.MagickWandGenesis()
    
    import atexit
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


@memoized
def __raw_lena():
        filename = join(dirname(__file__), 'lena.ycbcr.bz2')
        return dict(raw=bz2_readfile(filename), format='ycbcr',
                    height=512, width=512, depth=8)

# weakref memoization to let garbage collector clear it when needed
# helps pypy a lot
__lena = None


def __lena_image():
    global __lena
    
    if not __lena:
        lena = image.read_raw(**__raw_lena())
        __lena = weakref.ref(lena)
    else:
        lena = __lena()
        if not lena:
            lena = image.read_raw(**__raw_lena())
            __lena = weakref.ref(lena)
    
    return lena.copy()


def lena(size=None, colorspace=None):
    img = __lena_image()
    
    if size:
        img.resize(size, size)
    if not colorspace:
        colorspace = image.colorspace.rgb
    if img.colorspace != colorspace:
        img.convert_colorspace(colorspace)
        
    return img


def magick_logo():
    return image.read_special('logo:')

import tinyimg.api.enum as enum_api


def enum_lookup(mnemonic, throw=True):
    value = enum_api.lookup(mnemonic, magick.get_version())
    if throw and value == None:
        template = "Enumeration '{enum}' cant map mnemonic '{mnemonic}'"
        template = formattable(template)
        enum = mnemonic.enum.name
        mnemonic = mnemonic.name
        raise TinyException(template.format(enum=enum, mnemonic=mnemonic))

    return value


def enum_reverse_lookup(enum, value):
    return enum_api.reverse_lookup(enum, value, magick.get_version())


cdll = None

import weakref
from os.path import dirname, join

from tinyimg.compat import formattable, bz2_readfile
from tinyimg.util import TinyException

init()

from tinyimg import magick
from tinyimg import image
