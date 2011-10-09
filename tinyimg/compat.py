try:
    format
except NameError:
    from stringformat import FormattableString
    formattable = FormattableString
else:
    formattable = str

from six import PY3

if PY3:
    native_str = lambda v: v.decode('utf-8')
else:
    native_str = lambda v: v

import platform

dist = None
if hasattr(platform, 'linux_distribution'):
    dist = platform.linux_distribution
elif hasattr(platform, 'dist'):
    dist = platform.dist

try:
    import bz2
except ImportError:
    def bz2_readfile(filename):
        tempdir = gettempdir()
        template = formattable('cp "{src}" "{tmp}"')
        system(template.format(src=filename, tmp=tempdir))
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

# python <=2.6 doesnt have c_ssize_t,
# implementation copied from ctypes from 2.7
try:
    from ctypes import c_ssize_t
except ImportError:
    from ctypes import (c_void_p, c_int, c_long, c_longlong,
                        sizeof, c_uint, c_ulong, c_ulonglong)
    
    if sizeof(c_uint) == sizeof(c_void_p):
        c_ssize_t = c_int
    elif sizeof(c_ulong) == sizeof(c_void_p):
        c_ssize_t = c_long
    elif sizeof(c_ulonglong) == sizeof(c_void_p):
        c_ssize_t = c_longlong


from tempfile import gettempdir
from os import system, chdir, getcwd
from os.path import basename
