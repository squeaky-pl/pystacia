# coding: utf-8
# pystacia/api/func.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


def annote(cdll):
    cdll.MagickGetVersion.restype = c_char_p
    cdll.MagickGetVersion.argtypes = (POINTER(c_size_t),)
    
    cdll.MagickQueryConfigureOptions.restype = POINTER(c_char_p)
    cdll.MagickQueryConfigureOptions.argtypes = (c_char_p, POINTER(c_size_t))
    
    cdll.MagickQueryConfigureOption.restype = c_char_p
    cdll.MagickQueryConfigureOption.argtypes = (c_char_p,)
    
    cdll.MagickWandGenesis.restype = None
    cdll.MagickWandGenesis.argtypes = ()
    
    cdll.MagickWandTerminus.argtypes = ()
    cdll.MagickWandTerminus.restype = None
    
    #memory
    cdll.MagickRelinquishMemory.restype = c_void_p
    cdll.MagickRelinquishMemory.argtypes = (c_void_p,)
    
    #exceptions
    cdll.MagickGetException.restype = c_void_p
    cdll.MagickGetException.argtypes = (MagickWand_p, POINTER(ExceptionType))
    
    #wand
    cdll.NewMagickWand.restype = MagickWand_p
    cdll.NewMagickWand.argtypes = ()
    
    cdll.CloneMagickWand.restype = MagickWand_p
    cdll.CloneMagickWand.argtypes = (MagickWand_p,)
    
    cdll.DestroyMagickWand.restype = MagickWand_p
    cdll.DestroyMagickWand.argtypes = (MagickWand_p,)
    
    #properties
    
    #reading
    cdll.MagickReadImage.restype = MagickBoolean
    cdll.MagickReadImage.argtypes = (MagickWand_p, c_char_p)
    
    cdll.MagickReadImageBlob.restype = MagickBoolean
    cdll.MagickReadImageBlob.argtypes = (MagickWand_p, c_void_p, c_size_t)
    
    #writing
    cdll.MagickWriteImage.restype = MagickBoolean
    cdll.MagickWriteImage.argtypes = (MagickWand_p, c_char_p)
    
    cdll.MagickGetImageBlob.argtypes = (MagickWand_p, POINTER(c_size_t))
    cdll.MagickGetImageBlob.restype = c_void_p
    
    #properties
    cdll.MagickGetImageFormat.argtypes = (MagickWand_p,)
    cdll.MagickGetImageFormat.restype = c_char_p
    
    cdll.MagickSetImageFormat.argtypes = (MagickWand_p, c_char_p)
    cdll.MagickSetImageFormat.restype = MagickBoolean
    
    cdll.MagickGetFormat.argtypes = (MagickWand_p,)
    cdll.MagickGetFormat.restype = c_char_p
    
    cdll.MagickSetImageCompression.argtypes = (MagickWand_p, enum)
    cdll.MagickSetImageCompression.restype = MagickBoolean
    
    cdll.MagickGetImageCompression.argtypes = (MagickWand_p,)
    cdll.MagickGetImageCompression.restype = enum
    
    cdll.MagickSetFormat.argtypes = (MagickWand_p, c_char_p)
    cdll.MagickSetFormat.restype = MagickBoolean
    
    cdll.MagickSetDepth.argtypes = (MagickWand_p, c_size_t)
    cdll.MagickSetDepth.restype = MagickBoolean
    
    cdll.MagickGetImageCompressionQuality.argtypes = (MagickWand_p,)
    cdll.MagickGetImageCompressionQuality.restype = c_size_t
    
    cdll.MagickSetImageCompressionQuality.argtypes = (MagickWand_p, c_size_t)
    cdll.MagickSetImageCompressionQuality.restype = MagickBoolean
    
    cdll.MagickSetImageDepth.argtypes = (MagickWand_p, c_size_t)
    cdll.MagickSetImageDepth.restype = MagickBoolean
    
    cdll.MagickSetImageType.argtypes = (MagickWand_p, c_size_t)
    cdll.MagickSetImageType.restype = MagickBoolean
    
    cdll.MagickGetImageType.argtypes = (MagickWand_p,)
    cdll.MagickGetImageType.restype = enum
    
    cdll.MagickSetSize.argtypes = (MagickWand_p, c_size_t, c_size_t)
    cdll.MagickSetSize.restype = MagickBoolean
    
    cdll.MagickGetImageColorspace.argtypes = (MagickWand_p,)
    cdll.MagickGetImageColorspace.restype = enum
    
    cdll.MagickSetImageColorspace.argtypes = (MagickWand_p, enum)
    cdll.MagickSetImageColorspace.restype = MagickBoolean
    
    cdll.MagickTransformImageColorspace.argtypes = (MagickWand_p, enum)
    cdll.MagickTransformImageColorspace.restype = MagickBoolean
    
    # symbol added in 6.6.1.6
    try:
        cdll.MagickSetImageColor.argtypes = (MagickWand_p, PixelWand_p)
    except AttributeError:
        pass
    else:
        cdll.MagickSetImageColor.restype = MagickBoolean
    
    #size
    cdll.MagickGetImageWidth.restype = c_size_t
    cdll.MagickGetImageWidth.argtypes = (MagickWand_p,)
    
    cdll.MagickGetImageHeight.restype = c_size_t
    cdll.MagickGetImageHeight.argtypes = (MagickWand_p,)
    
    cdll.MagickGetImageDepth.restype = c_size_t
    cdll.MagickGetImageDepth.argtypes = (MagickWand_p,)
    
    #resize
    cdll.MagickResizeImage.argtypes = (MagickWand_p, c_size_t, c_size_t,
                                       enum, c_double)
    cdll.MagickResizeImage.restype = MagickBoolean
    
    #crop
    cdll.MagickCropImage.argtypes = (MagickWand_p, c_size_t, c_size_t,
                                     c_ssize_t, c_ssize_t)
    cdll.MagickCropImage.restype = MagickBoolean
    
    #flip
    cdll.MagickFlipImage.argtypes = (MagickWand_p,)
    cdll.MagickFlipImage.restype = MagickBoolean
    
    cdll.MagickFlopImage.argtypes = (MagickWand_p,)
    cdll.MagickFlopImage.restype = MagickBoolean
    
    #roll
    cdll.MagickRollImage.argtypes = (MagickWand_p, c_ssize_t, c_ssize_t)
    cdll.MagickRollImage.restype = MagickBoolean
    
    #other
    cdll.MagickDespeckleImage.argtypes = (MagickWand_p,)
    cdll.MagickDespeckleImage.restype = MagickBoolean
    
    cdll.MagickEmbossImage.argtypes = (MagickWand_p, c_double, c_double)
    cdll.MagickEmbossImage.restype = MagickBoolean
    
    cdll.MagickEnhanceImage.argtypes = (MagickWand_p,)
    cdll.MagickEnhanceImage.restype = MagickBoolean
    
    cdll.MagickEqualizeImage.argtypes = (MagickWand_p,)
    cdll.MagickEqualizeImage.restype = MagickBoolean
    
    cdll.MagickForwardFourierTransformImage.argtypes = (MagickWand_p,
                                                        MagickBoolean)
    cdll.MagickForwardFourierTransformImage.restype = MagickBoolean
    
    cdll.MagickNextImage.argtypes = (MagickWand_p,)
    cdll.MagickNextImage.restype = MagickBoolean
    
    cdll.MagickFxImage.argtypes = (MagickWand_p, c_char_p)
    cdll.MagickFxImage.restype = MagickWand_p
    
    cdll.MagickGammaImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickGammaImage.restype = MagickBoolean
    
    cdll.MagickSwirlImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickSwirlImage.restype = MagickBoolean
    
    cdll.MagickSpreadImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickSpreadImage.restype = MagickBoolean
    
    cdll.MagickAutoGammaImage.argtypes = (MagickWand_p,)
    cdll.MagickAutoGammaImage.restype = MagickBoolean
    
    cdll.MagickAutoLevelImage.argtypes = (MagickWand_p,)
    cdll.MagickAutoLevelImage.restype = MagickBoolean
    
    cdll.MagickBlurImage.argtypes = (MagickWand_p, c_double, c_double)
    cdll.MagickBlurImage.restype = MagickBoolean
    
    cdll.MagickBrightnessContrastImage.argtypes = (MagickWand_p, c_double,
                                                   c_double)
    cdll.MagickBrightnessContrastImage.restype = MagickBoolean
    
    cdll.MagickCompositeImage.argtypes = (MagickWand_p, MagickWand_p, enum,
                                          c_ssize_t, c_ssize_t)
    cdll.MagickCompositeImage.restype = MagickBoolean
    
    cdll.MagickDeskewImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickDeskewImage.restype = MagickBoolean
    
    cdll.MagickModulateImage.argtypes = (MagickWand_p, c_double,
                                         c_double, c_double)
    cdll.MagickModulateImage.restype = MagickBoolean
    
    cdll.MagickNegateImage.argtypes = (MagickWand_p, MagickBoolean)
    cdll.MagickNegateImage.restype = MagickBoolean
    
    cdll.MagickOilPaintImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickOilPaintImage.restype = MagickBoolean
    
    cdll.MagickPosterizeImage.argtypes = (MagickWand_p, c_uint, MagickBoolean)
    cdll.MagickPosterizeImage.restype = MagickBoolean
    
    cdll.MagickRadialBlurImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickRadialBlurImage.restype = MagickBoolean
    
    cdll.MagickRotateImage.argtypes = (MagickWand_p, PixelWand_p, c_double)
    cdll.MagickRotateImage.restype = MagickBoolean
    
    cdll.MagickSepiaToneImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickSepiaToneImage.restype = MagickBoolean
    
    cdll.MagickSetImageOpacity.argtypes = (MagickWand_p, c_double)
    cdll.MagickSetImageOpacity.restype = MagickBoolean
    
    cdll.MagickWaveImage.argtypes = (MagickWand_p, c_double, c_double)
    cdll.MagickWaveImage.restype = MagickBoolean
    
    cdll.MagickShadowImage.argtypes = (MagickWand_p, c_double, c_double,
                                       c_ssize_t, c_ssize_t)
    cdll.MagickShadowImage.restype = MagickBoolean
    
    cdll.MagickShearImage.argtypes = (MagickWand_p, PixelWand_p,
                                      c_double, c_double)
    cdll.MagickShearImage.restype = MagickBoolean
    
    cdll.MagickSketchImage.argtypes = (MagickWand_p, c_double,
                                       c_double, c_double)
    cdll.MagickSketchImage.restype = MagickBoolean
    
    cdll.MagickSolarizeImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickSolarizeImage.restype = MagickBoolean
    
    cdll.MagickTransposeImage.argtypes = (MagickWand_p,)
    cdll.MagickTransposeImage.restype = MagickBoolean
    
    cdll.MagickTransverseImage.argtypes = (MagickWand_p,)
    cdll.MagickTransverseImage.restype = MagickBoolean
    
    cdll.MagickColorizeImage.argtypes = (MagickWand_p, PixelWand_p,
                                         PixelWand_p)
    cdll.MagickColorizeImage.restype = MagickBoolean
    
    cdll.MagickGetImagePixelColor.argtypes = (MagickWand_p, c_ssize_t,
                                              c_ssize_t, PixelWand_p)
    cdll.MagickGetImagePixelColor.restype = MagickBoolean
    
    cdll.MagickSpliceImage.argtypes = (MagickWand_p, c_size_t, c_size_t,
                                       c_ssize_t, c_ssize_t)
    cdll.MagickSpliceImage.restype = MagickBoolean
    
    cdll.MagickSetImageBackgroundColor.argtypes = (MagickWand_p, PixelWand_p)
    cdll.MagickSetImageBackgroundColor.restype = MagickBoolean
    
    cdll.MagickGetImageBackgroundColor.argtypes = (MagickWand_p, PixelWand_p)
    cdll.MagickGetImageBackgroundColor.restype = MagickBoolean
    
    cdll.MagickTrimImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickTrimImage.restype = MagickBoolean
    
    ###pixelwand
    cdll.NewPixelWand.argtypes = ()
    cdll.NewPixelWand.restype = PixelWand_p
    
    cdll.DestroyPixelWand.argtypes = (PixelWand_p,)
    cdll.DestroyPixelWand.restype = PixelWand_p
    
    cdll.ClonePixelWand.argtypes = (PixelWand_p,)
    cdll.ClonePixelWand.restype = PixelWand_p
    
    cdll.PixelSetColor.argtypes = (PixelWand_p, c_char_p)
    cdll.PixelSetColor.restype = MagickBoolean
    
    cdll.PixelSetRed.argtypes = (PixelWand_p, c_double)
    cdll.PixelSetRed.restype = None
    
    cdll.PixelSetGreen.argtypes = (PixelWand_p, c_double)
    cdll.PixelSetGreen.restype = None
    
    cdll.PixelSetBlue.argtypes = (PixelWand_p, c_double)
    cdll.PixelSetBlue.restype = None
    
    cdll.PixelSetAlpha.argtypes = (PixelWand_p, c_double)
    cdll.PixelSetAlpha.restype = None
    
    cdll.PixelGetRed.argtypes = (PixelWand_p,)
    cdll.PixelGetRed.restype = c_double
    
    cdll.PixelGetGreen.argtypes = (PixelWand_p,)
    cdll.PixelGetGreen.restype = c_double
    
    cdll.PixelGetBlue.argtypes = (PixelWand_p,)
    cdll.PixelGetBlue.restype = c_double
    
    cdll.PixelGetAlpha.argtypes = (PixelWand_p,)
    cdll.PixelGetAlpha.restype = c_double


def guard(wand, callable, msg=None):  # @ReservedAssignment
    result = callable()
    if not result:
        description = None
        if not msg:
            exc_type = ExceptionType()
            description = cdll.MagickGetException(wand, byref(exc_type))
            msg = cast(description, c_char_p).value
        exc = TinyException(msg)
        
        if description:
            cdll.MagickRelinquishMemory(description)
        
        raise exc
        
    return result


from ctypes import (c_char_p, c_void_p, POINTER, byref,
                    cast, c_size_t, c_double, c_uint)

from pystacia.util import TinyException
from pystacia.compat import c_ssize_t
from pystacia import cdll
from pystacia.api.type import (MagickWand_p, PixelWand_p, MagickBoolean,
                           ExceptionType, enum)
