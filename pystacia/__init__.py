# coding: utf-8
# pystacia/__init__.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""pystacia is a raster graphics library utilizing ImageMagick."""


__version__ = '0.3dev'
__author__ = 'Pawel Piotr Przeradowski'


from os import environ

if not environ.get('PYSTACIA_SETUP'):
    from logging import getLogger, basicConfig
    
    logger = getLogger('pystacia')
    
    level = environ.get('PYSTACIA_LOG')
    if level:
        level = int(level)
        format = '%(asctime)s %(name)-12s %(thread)d %(message)s'
        basicConfig(level=level, format=format)
    
    logger.debug('Imported main module')
    
    if environ.get('PYSTACIA_TRACE'):
        logger.debug('Starting tracing')
        import stacktracer
        stacktracer.trace_start('trace.html', interval=5, auto=True)
    
    from pystacia.registry import Registry
    
    registry = Registry()
    
    from pystacia import color
    
    colors = color.Factory()
    """Convenience factory for SVG names"""
    
    def lazy_imported(key):
        def call(*args, **kw):
            from pystacia import image
            
            return getattr(image, key)(*args, **kw)
        
        return call
    
    def really_lazy_enum(key):
        class Proxy(object):
            def __init__(self, key):
                self.__key = key
                
            def __getattr__(self, attr_key):
                from pystacia import image
                
                enum = getattr(image, key)
                return getattr(enum, attr_key)
            
        return Proxy(key)
    
    # lazy importing proxies
    read = lazy_imported('read')
    read_blob = lazy_imported('read_blob')
    read_raw = lazy_imported('read_raw')
    blank = lazy_imported('blank')
    checkerboard = lazy_imported('checkerboard')
    lena = lazy_imported('lena')
    magick_logo = lazy_imported('magick_logo')
    rose = lazy_imported('rose')
    wizard = lazy_imported('wizard')
    granite = lazy_imported('granite')
    netscape = lazy_imported('netscape')
    Image = lazy_imported('Image')
    
    composites = really_lazy_enum('composites')
    types = really_lazy_enum('types')
    filters = really_lazy_enum('filters')
    colorspaces = really_lazy_enum('colorspaces')
    compressions = really_lazy_enum('compressions')
    axes = really_lazy_enum('axes')
    
    __all__ = [
        'read', 'read_blob', 'read_raw',
        'blank', 'checkerboard',
        'lena', 'magick_logo', 'rose', 'wizard', 'granite', 'netscape',
        'composites', 'types', 'filters',
        'colorspaces', 'compressions', 'axes',
        'color', 'colors',
        'Image',
        
        'registry']
    
    from zope.deprecation import deprecated
    from pystacia.compat import formattable
    
    msg = formattable('Use pystacia.image.{0} instead')
    for symbol in set(__all__) - set(['color', 'colors', 'registry']):
        deprecated(symbol, msg.format(symbol))
