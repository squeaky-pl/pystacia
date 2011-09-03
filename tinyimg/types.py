from ctypes import Structure, POINTER, py_object, c_int

enum = c_int

MagickBoolean = enum
ExceptionType = enum

# taken from http://svn.python.org/projects/ctypes/trunk/ctypeslib/ctypeslib/contrib/pythonhdr.py
try:
    import ctypes.pythonapi
except ImportError: pass
else:
    class FILE(Structure): pass
    FILE_p = POINTER(FILE)

    as_FILE_p = ctypes.pythonapi.PyFile_AsFile
    as_FILE_p.restype = FILE_p
    as_FILE_p.argtypes = (py_object,)

class MagickWand(Structure): pass
MagickWand_p = POINTER(MagickWand)
