try:
    from unittest import skip, skipIf
except ImportError:
    from unittest2 import skip, skipIf  # @UnusedImport @Reimport

from unittest import TestCase
if not hasattr(TestCase, 'assertSequenceEqual'):
    from unittest2 import TestCase  # @UnusedImport @Reimport