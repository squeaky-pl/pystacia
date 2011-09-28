from ctypes import Structure, POINTER, py_object, c_int, c_size_t, c_char

enum = c_int

MaxText = c_char * 4096

class Filter(enum): pass

filters = ('UNDEFINED',
           'POINT',
           'BOX',
           'TRIANGLE',
           'HERMITE',
           'HANNING',
           'HAMMING',
           'BLACKMAN',
           'GAUSSIAN',
           'QUADRATIC',
           'CUBIC',
           'CATROM',
           'MITCHELL',
           'JINC',
           'SINC',
           'KAISER',
           'WELSH',
           'PARZEN',
           'BOHMAN',
           'BARTLETT',
           'LAGRANGE',
           'LANCZOS',
           'LANCZOS_SHARP',
           'LANCZOS2',
           'LANCZOS2_SHARP',
           'ROBIDOUX'
           )
for i, filter in enumerate(filters): setattr(Filter, filter, i)

MagickBoolean = enum
ExceptionType = enum

class ExceptionInfo(Structure): pass
class ImageInfo(Structure): pass
class QuantizeInfo(Structure): pass
class Image(Structure): pass

class MagickWand(Structure):
    _fields_ = (('id', c_size_t),
                ('name', MaxText),
                ('exception', POINTER(ExceptionInfo)),
                ('image_info', POINTER(ImageInfo)),
                ('quantize_info', POINTER(QuantizeInfo)),
                ('images', POINTER(Image)),
                ('active', MagickBoolean),
                ('pend', MagickBoolean),
                ('debug', MagickBoolean),
                ('signature', c_size_t))
MagickWand_p = POINTER(MagickWand)

class PixelWand(Structure): pass
PixelWand_p = POINTER(PixelWand)