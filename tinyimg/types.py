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

class Composite(enum): pass
operators = ('ATOP',
             'BLEND',
             'BLUR',
             'BUMPMAP',
             'CHANGE_MASK',
             'CLEAR',
             'COLOR_BURN',
             'COLOR_DODGE',
             'COLORIZE',
             'COPY_BLACK',
             'COPY_BLUE',
             'COPY_COMPOSITE',
             'COPY_CYAN',
             'COPY_GREEN',
             'COPY_MAGENTA',
             'COPY_OPACITY',
             'COPY_RED',
             'COPY_YELLOW',
             'DARKEN',
             'DARKEN_INTENSITY',
             'DIFFERENCE',
             'DISPLACE',
             'DISSOLVE',
             'DISTORT',
             'DIVIDE_DST',
             'DIVIDE_SRC',
             'DST_ATOP',
             'DST',
             'DST_IN',
             'DST_OUT',
             'DST_OVER',
             'EXCLUSION',
             'HARD_LIGHT',
             'HUE',
             'IN',
             'LIGHTEN',
             'LIGHTEN_INTENSITY',
             'LINEAR_BURN',
             'LINEAR_DODGE',
             'LINEAR_LIGHT',
             'LUMINIZE',
             'MATHEMATICS',
             'MINUS_DST',
             'MINUS_SRC',
             'MODULATE',
             'MODULATE_ADD',
             'MODULATE_SUBSTRACT',
             'MULTIPLY',
             'NO',
             'OUT',
             'OVER',
             'OVERLAY',
             'PEGTOP',
             'PIN_LIGHT',
             'PLUS',
             'REPLACE',
             'SATURATE',
             'SCREEN',
             'SOFT_LIGHT',
             'SRC_ATOP',
             'SRC_COMPOSITE',
             'SRC_IN',
             'SRC_OUT',
             'SRC_OVER',
             'THRESHOLD',
             'UNDEFINED',
             'VIVID_LIGHT',
             'XOR')

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
