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

# detect PyPy
import sys
pypy = '__pypy__' in sys.builtin_module_names

# detect Jython
jython = sys.platform.startswith('java')

if jython:
    from java.io import File  # @UnresolvedImport
    from java.net import URL  # @UnresolvedImport
    from javax.imageio import ImageIO  # @UnresolvedImport
    from javax.swing import JLabel, JFrame, ImageIcon  # @UnresolvedImport

    def gui_open(path):
        label = JLabel(ImageIcon(ImageIO.read(File(URL(path).getFile()))))
        frame = JFrame()
        frame.getContentPane().add(label)
        frame.pack()
        frame.setLocation(200, 200)
        frame.setVisible(True)
else:
    from webbrowser import open as gui_open  # NOQA
