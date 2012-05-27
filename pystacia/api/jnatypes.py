import ctypes

from java.lang import UnsatisfiedLinkError  # @UnresolvedImport
from com.sun.jna import NativeLibrary, Pointer  # @UnresolvedImport

from pystacia.util import memoized


class c_void_p(object):
    _wrap = True
    _unwrap = True
    _jffi_type = ctypes.c_ulong._jffi_type

    def __init__(self, value):
        self.value = value

    def __long__(self):
        return self.value


class c_char_p_p(object):
    _wrap = True
    _jffi_type = ctypes.c_void_p._jffi_type

    def __init__(self, value):
        self.value = Pointer(value)

    def __getitem__(self, idx):
        return string_at(self.value.getPointer(idx * Pointer.SIZE))


def POINTER(type):  # @ReservedAssignment
    if type == ctypes.c_char_p:
        return c_char_p_p
    else:
        return ctypes.POINTER(type)


def string_at(p, length=None):
    if isinstance(p, c_void_p):
        p = Pointer(p.value)

    if length:
        return p.getByteArray(0, length).tostring()

    return p.getString(0).encode('utf-8')


class Function(object):
    def __init__(self, func):
        self.__dict__['_func'] = func

    def __call__(self, *args):
        func = self._func

        result = func(*args)

        if hasattr(func.restype, '_wrap'):
            result = func.restype(result)

        return result

    def __getattr__(self, name):
        return getattr(self._func, name)

    def __setattr__(self, name, value):
        setattr(self._func, name, value)


class Library(object):
    def __init__(self, path):
        self._dll = ctypes.CDLL(path)
        self._name = path

    @memoized
    def __getattr__(self, name):
        try:
            return Function(getattr(self._dll, name))
        except NameError, e:
            raise AttributeError(e)


@memoized
def CDLL(path):
    return Library(path)


def find_library(name):
    # this fallback is good enough ;-)
    try:
        library = NativeLibrary.getInstance(name)
    except UnsatisfiedLinkError:
        return None

    return library.file.path
