# coding: utf-8

# pystacia/api/func.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from threading import Lock

from six import b as bytes_, text_type

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


if pypy:
    __lock = Lock()


def handle_result(result, restype, args, argtypes):
    if restype == c_char_p:
        result = native_str(result)
    if restype in (c_uint, c_ssize_t, c_size_t):
        result = int(result)
    elif restype == enum and not jython:
        result = result.value
    elif restype == MagickBoolean and not result:
        exc_type = ExceptionType()

        if argtypes[0] == MagickWand_p:
            klass = 'magick'
        elif argtypes[0] == PixelWand_p:
            klass = 'pixel'

        description = c_call(klass, 'get_exception', args[0], byref(exc_type))
        try:
            raise PystaciaException(native_str(string_at(description)))
        finally:
            c_call('magick_', 'relinquish_memory', description)

    return result


def prepare_args(c_method, obj, args):
    keep_ = []
    args_ = []
    should_lock = False

    if isinstance(obj, Resource):
        args = (obj,) + args

    for arg, type in zip(args, c_method.argtypes):  # @ReservedAssignment
        if type == c_char_p:
            should_lock = True
            if isinstance(arg, text_type):
                arg = bytes_(arg)
        elif type in (c_size_t, c_ssize_t, c_uint):
            arg = int(arg)
        elif type == PixelWand_p and not isinstance(arg, PixelWand_p):
            arg = color_cast(arg)
            keep_.append(arg)

        if isinstance(arg, Resource):
            arg = arg.resource

        args_.append(arg)

    return keep_, args_, should_lock


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

    # if objects are casted here and then
    # there is only their resource passed
    # there is a risk that GC will collect
    # them and __del__ will be called between
    # driving Imagick to SIGSEGV
    # lets keep references to them
    keep_, args_, should_lock = prepare_args(c_method, obj, args)

    msg = formattable('Calling {0}')
    logger.debug(msg.format(method_name))

    if pypy and should_lock:
        __lock.acquire()

    result = c_method(*args_)

    if pypy and should_lock:
        __lock.release()

    del keep_

    return handle_result(
        result, c_method.restype, args_, c_method.argtypes)


from pystacia.util import PystaciaException
from pystacia.compat import native_str, formattable, jython
from pystacia.api import get_dll, logger
from pystacia.api.type import (
    MagickWand_p, PixelWand_p, MagickBoolean, ExceptionType, enum)
from pystacia.api.compat import (
    c_char_p, c_size_t, c_uint, string_at, c_ssize_t, byref)
from pystacia.common import Resource
from pystacia.color import cast as color_cast
