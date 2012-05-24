# coding: utf-8

# pystacia/compat.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import absolute_import

try:
    format
except NameError:
    from stringformat import FormattableString  # @UnresolvedImport
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
    from webbrowser import open as gui_open
except ImportError:
    #TODO: implement
    gui_open = lambda x: None


# detect PyPy
import sys
pypy = '__pypy__' in sys.builtin_module_names
