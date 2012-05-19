# coding: utf-8
# pystacia/image/_impl/__init__.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


def alloc(image):
    return c_call('wand', 'new')


def free(image):
    return c_call('wand', 'destroy', image)


def clone(image):
    return c_call('wand', 'clone', image)


from pystacia.api.func import c_call
