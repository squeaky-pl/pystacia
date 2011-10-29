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


def fallback_bz2_readfile(filename):
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


def bz2_readfile(filename):
    f = bz2.BZ2File(filename, 'rb')
    data = f.read()
    f.close()
    
    return data

try:
    import bz2
except ImportError:
    bz2_readfile = fallback_bz2_readfile


# python <=2.6 doesnt have c_ssize_t,
# implementation copied from ctypes from 2.7
def fallback_c_size_t():
    from ctypes import (c_void_p, c_int, c_long, c_longlong,
                        sizeof, c_uint, c_ulong, c_ulonglong)
    
    if sizeof(c_uint) == sizeof(c_void_p):
        return c_int
    elif sizeof(c_ulong) == sizeof(c_void_p):
        return c_long
    elif sizeof(c_ulonglong) == sizeof(c_void_p):
        return c_longlong
        
import ctypes
c_ssize_t = getattr(ctypes, 'c_ssize_t', fallback_c_size_t())


try:
    from unittest import skip, skipIf
except ImportError:
    from unittest2 import skip, skipIf  # @UnusedImport @Reimport

from unittest import TestCase
if not hasattr(TestCase, 'assertSequenceEqual'):
    from unittest2 import TestCase  # @UnusedImport @Reimport

from tempfile import gettempdir
from os import system, chdir, getcwd
from os.path import basename
