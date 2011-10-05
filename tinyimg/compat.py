from bz2 import BZ2File

# patch BZ2File to support with statement in python <=2.6
if not hasattr(BZ2File, '__exit__'):
    class BZ2Replacement(BZ2File):
        __enter__ = lambda self: self
        __exit__ = lambda self, type, value, traceback: self.close()
        
    BZ2File = BZ2Replacement

# formattable, needed for python 2.5
try: format
except NameError:
    from stringformat import FormattableString
    formattable = FormattableString
else:
    formattable = str

from six import PY3

if PY3: decode_char_p = lambda v: v.decode('utf-8')
else: decode_char_p = lambda v: v
