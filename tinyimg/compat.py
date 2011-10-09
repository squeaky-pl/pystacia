try: format
except NameError:
    from stringformat import FormattableString
    formattable = FormattableString
else:
    formattable = str

from six import PY3

if PY3: native_str = lambda v: v.decode('utf-8')
else: native_str = lambda v: v

import platform

dist = None
if hasattr(platform, 'linux_distribution'):
    dist = platform.linux_distribution
elif hasattr(platform, 'dist'):
    dist = platform.dist

try: import bz2
except ImportError:
    def bz2_readfile(filename):
        tempdir = gettempdir()
        system(formattable('cp "{src}" "{tmp}"').format(src=filename, tmp=tempdir))
        olddir = getcwd()
        chdir(tempdir)
        filename = basename(filename)
        system(formattable('bunzip2 {0}').format(filename))
        
        filename = filename[:-4]
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        
        chdir(olddir)
        
        return data
else:
    def bz2_readfile(filename):
        f = bz2.BZ2File(filename, 'rb')
        data = f.read()
        f.close()
        
        return data

from tempfile import gettempdir
from os import system, chdir, getcwd
from os.path import basename
