from ctypes import Structure, POINTER, c_int


enum = c_int
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
