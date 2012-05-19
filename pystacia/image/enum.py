# coding: utf-8

# pystacia/image/enum.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pystacia.lazyenum import enum


types = enum('type')
filters = enum('filter')
colorspaces = enum('colorspace')
compressions = enum('compression')
composites = enum('composite')
axes = enum('axis')
metrics = enum('metric')
noises = enum('noise')
thresholds = enum('threshold')
interpolations = enum('interpolation')
operations = enum('operation')
fit_modes = enum('mode')
