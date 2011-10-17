from tinyimg.util import memoized


@memoized
def get_version():
    options = get_options()
    
    try:
        version = options['LIB_VERSION_NUMBER']
    except KeyError:
        try:
            version = options['VERSION']
        except KeyError:
            return None
        else:
            return tuple(int(x) for x in version.split('.'))
    else:
        return tuple(int(x) for x in version.split(','))


@memoized
def get_options():
    options = {}
    
    from ctypes import c_size_t
    from six import b
    from tinyimg.compat import native_str
    
    size = c_size_t()
    keys = cdll.MagickQueryConfigureOptions(b('*'), size)
    for key in (keys[i] for i in range(size.value)):
        options[native_str(key)] =\
        native_str(cdll.MagickQueryConfigureOption(key))
            
    return options


def get_version_str():
    return cdll.MagickGetVersion(None)


def get_delegates():
    try:
        delegates = get_options()['DELEGATES']
    except KeyError:
        return []
    
    return delegates.split()

from tinyimg import cdll
