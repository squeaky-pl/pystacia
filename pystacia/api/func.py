# coding: utf-8

# pystacia/api/func.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from threading import Lock

from six import string_types, b as bytes_, text_type

from pystacia.util import memoized
from pystacia.compat import pypy
from pystacia.api.metadata import data as metadata


@memoized
def get_c_method(api_type, method, throw=True):
    type_data = metadata[api_type]
    method_name = type_data['format'](method)

    if not throw and not hasattr(get_dll(False), method_name):
        return False

    c_method = getattr(get_dll(False), method_name)

    msg = formattable('Annoting {0}')
    logger.debug(msg.format(method_name))
    method_data = type_data['symbols'][method]

    argtypes = method_data[0]
    if 'arg' in type_data:
        argtypes = (type_data['arg'],) + argtypes
    c_method.argtypes = argtypes

    restype = type_data.get('result', None)
    if len(method_data) == 2:
        restype = method_data[1]
    c_method.restype = restype

    return method_name, c_method


def annote():
    dll = get_dll()

    for class_, funcs in get_data().items():
        for name in funcs['symbols']:
            get_c_method(class_, name)

    return dll

if pypy:
    __lock = Lock()


def c_call(obj, method, *args, **kw):
    if hasattr(obj.__class__, '_api_type'):
        api_type = obj.__class__._api_type
    else:
        api_type = obj

    msg = formattable('Translating method {0}.{1}')
    logger.debug(msg.format(api_type, method))

    method_name, c_method = get_c_method(api_type, method)

    try:
        init = kw.pop('__init')
    except KeyError:
        init = True

    if init:
        get_dll()

    if isinstance(obj, Resource):
        args = (obj,) + args

    # if objects are casted here and then
    # there is only their resource passed
    # there is a risk that GC will collect
    # them and __del__ will be called between
    # driving Imagick to SIGSEGV
    # lets keep references to them
    keep_ = []
    args_ = []
    should_lock = False
    for arg, type in zip(args, c_method.argtypes):  # @ReservedAssignment
        if type == c_char_p:
            should_lock = True
            if isinstance(arg, text_type):
                arg = bytes_(arg)
        elif type in (c_size_t, c_ssize_t, c_uint):
            arg = int(arg)
        elif type == PixelWand_p:
            arg = color_cast(arg)
            keep_.append(arg)

        if isinstance(arg, Resource):
            arg = arg.resource

        args_.append(arg)

    msg = formattable('Calling {0}')
    logger.debug(msg.format(method_name))

    if pypy and should_lock:
        __lock.acquire()

    result = c_method(*args_)

    if pypy and should_lock:
        __lock.release()

    if c_method.restype == c_char_p:
        result = native_str(result)
    if c_method.restype in (c_uint, c_ssize_t, c_size_t):
        result = int(result)
    elif c_method.restype == enum and not jython:
        result = result.value
    elif c_method.restype == MagickBoolean and not result:
        exc_type = ExceptionType()

        if c_method.argtypes[0] == MagickWand_p:
            class_ = 'magick'
        elif c_method.argtypes[0] == PixelWand_p:
            class_ = 'pixel'

        description = c_call(class_, 'get_exception', args[0], byref(exc_type))
        try:
            raise PystaciaException(native_str(string_at(description)))
        finally:
            c_call('magick_', 'relinquish_memory', description)

    return result

from pystacia.util import PystaciaException
from pystacia.compat import native_str, formattable, jython
from pystacia.api import get_dll, logger
from pystacia.api.type import (
    MagickWand_p, PixelWand_p, MagickBoolean, ExceptionType, enum)
from pystacia.api.compat import (c_char_p, c_void_p, POINTER, c_size_t,
                                 c_double, c_uint, string_at, c_ssize_t, byref)
from pystacia.common import Resource
from pystacia.color import cast as color_cast
