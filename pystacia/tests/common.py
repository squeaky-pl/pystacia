try:
    from unittest import skip, skipIf
except ImportError:
    from unittest2 import skip, skipIf  # @UnusedImport @Reimport

from unittest import TestCase
if not hasattr(TestCase, 'assertSequenceEqual'):
    from unittest2 import TestCase  # @UnusedImport @Reimport


from pystacia import image
from pystacia.image import types
from pystacia.image.sample import lena_available


if lena_available():
    sample = image.lena
    sample.size = (512, 512)
    sample.type = types.truecolor
else:
    sample = image.magick_logo
    sample.size = (640, 480)
    sample.type = types.palette