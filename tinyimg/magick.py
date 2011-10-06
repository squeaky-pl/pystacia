from tinyimg.util import memoized

@memoized
def get_version():
    options = get_options()
    
    try: version = options['LIB_VERSION_NUMBER']
    except KeyError:
        try: version = options['VERSION']
        except KeyError: return None
        else: return tuple(int(x) for x in version.split('.'))
    else: return tuple(int(x) for x in version.split(','))

@memoized
def get_options():
    options = {}
    
    size = c_size_t()
    keys = cdll.MagickQueryConfigureOptions(b('*'), size)
    for key in (keys[i] for i in range(size.value)):
        options[decode_char_p(key)] =\
        decode_char_p(cdll.MagickQueryConfigureOption(key))
            
    return options

def get_version_str():
    return cdll.MagickGetVersion(None)


from ctypes import c_size_t

from six import b 

from tinyimg import cdll
from tinyimg.compat import decode_char_p