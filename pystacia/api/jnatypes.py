from java.lang import Void, String, Integer, Double, UnsatisfiedLinkError  # @UnresolvedImport
from com.sun.jna import NativeLibrary, NativeLong, Pointer  # @UnresolvedImport
from com.sun.jna import ptr

from pystacia.util import memoized

__ref_mapping = {Integer: ptr.IntByReference,
                 NativeLong: ptr.NativeLongByReference,
                 Double: ptr.DoubleByReference}


class wrappable(object):
    def __init__(self, j_object=None):
            self.value = self._j_object = j_object


@memoized
def POINTER(type):  # @ReservedAssignment
    class pointer(wrappable):
        _j_type = Pointer
        _to = type

        def __getitem__(self, idx):
            deref = self._j_object.getPointer(idx * Pointer.SIZE)

            if issubclass(self._to, wrappable):
                deref = self._to(deref)

            if hasattr(deref, '_after'):
                deref = deref._after()

            return deref

    return pointer


class c_void(object):
    _j_type = Void


class c_char(object):
    pass

c_void_p = POINTER(c_void)


c_char_p = POINTER(c_char)
c_char_p._after = lambda o: str(o._j_object.getString(0))


class c_int(wrappable):
    _j_type = Integer


class c_uint(wrappable):
    _j_type = Integer


_after_size = lambda o: o._j_object.toNative()


class c_size_t(wrappable):
    _j_type = NativeLong
    _after = _after_size


class c_ssize_t(wrappable):
    _j_type = NativeLong
    _after = _after_size


class c_double(object):
    _j_type = Double


class Reference(object):
    def __init__(self, o):
        self._object = o
        self._j_object = __ref_mapping[o.__class__._j_type]()

    def sync(self):
        value = self._j_object.getValue()
        if isinstance(value, NativeLong):
            value = value.toNative()
        self._object.value = value


def byref(o):
    return Reference(o)


def string_at(p, length=None):
    if length:
        return p._j_object.getByteArray(0, length).tostring()

    return str(p._j_object.getString(0))


class Function(object):
    def __init__(self, java_function):
        self._j_function = java_function
        self.argtypes = None

    def __call__(self, *args):
        args_ = []
        to_sync = []
        for arg, type_ in zip(args, self.argtypes):
            if isinstance(arg, Reference):
                to_sync.append(arg)
            if hasattr(arg, '_j_object'):
                arg = arg._j_object
            if type_._j_type == NativeLong:
                arg = NativeLong(arg)
            args_.append(arg)

        result = self._j_function.invoke(self.restype._j_type, args_)

        [arg.sync() for arg in to_sync]

        if issubclass(self.restype, wrappable):
            result = self.restype(result)

        if hasattr(result, '_after'):
            result = result._after()

        return result


class Library(object):
    def __init__(self, java_library):
        self._j_library = java_library
        self._name = java_library.file.path

    @memoized
    def __getattr__(self, key):
        try:
            return Function(self._j_library.getFunction(key))
        except UnsatisfiedLinkError, e:
            raise AttributeError(e)


@memoized
def CDLL(path):
    return Library(NativeLibrary.getInstance(path))


def find_library(name):
    # this fallback is good enough ;-)
    try:
        library = NativeLibrary.getInstance(name)
    except UnsatisfiedLinkError:
        return None

    return library.file.path
