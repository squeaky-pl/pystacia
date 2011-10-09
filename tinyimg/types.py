from ctypes import Structure, POINTER, c_int, c_char


enum = c_int

MaxText = c_char * 4096

MagickBoolean = enum
ExceptionType = enum


class Image(Structure):
    pass


class MagickWand(Structure):
    pass
MagickWand_p = POINTER(MagickWand)


class PixelWand(Structure):
    pass
PixelWand_p = POINTER(PixelWand)
