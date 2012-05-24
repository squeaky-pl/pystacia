from java.lang import Void, String, Integer  # @UnresolvedImport
from com.sun.jna import NativeLibrary, NativeLong  # @UnresolvedImport
[ ]
from pystacia.util import memoized


class c_void(object):
    _j_type = Void


class c_char_p(object):
    _j_type = String


class c_int(object):
    _j_type = Integer


class c_size_t(object):
    _j_type = NativeLong


class Function(object):
    def __init__(self, java_function):
        self._j_function = java_function

    def __call__(self, *args):
        return self._j_function.invoke(self.restype._j_type, args)


class Library(object):
    def __init__(self, java_library):
        self._j_library = java_library

    @memoized
    def __getattr__(self, key):
        return Function(self._j_library.getFunction(key))


@memoized
def CDLL(path):
    return Library(NativeLibrary.getInstance(path))


def find_library(path):
    # this fallback is good enough ;-)
    return path
