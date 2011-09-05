from ctypes import c_char_p, c_void_p, POINTER, byref, cast, c_size_t, c_ssize_t, c_double

from . import TinyException, cdll
from .types import MagickWand_p, MagickBoolean, ExceptionType, Filter

def annote(cdll):
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
    
    cdll.MagickSetFormat.argtypes = (MagickWand_p, c_char_p)
    cdll.MagickSetFormat.restype = MagickBoolean
    
    cdll.MagickSetDepth.argtypes = (MagickWand_p, c_size_t)
    cdll.MagickSetDepth.restype = MagickBoolean
    
    cdll.MagickSetSize.argtypes = (MagickWand_p, c_size_t, c_size_t)
    cdll.MagickSetSize.restype = MagickBoolean
    
    #size
    cdll.MagickGetImageWidth.restype = c_size_t
    cdll.MagickGetImageWidth.argtypes = (MagickWand_p,)
    
    cdll.MagickGetImageHeight.restype = c_size_t
    cdll.MagickGetImageHeight.argtypes = (MagickWand_p,)
    
    cdll.MagickGetImageDepth.restype = c_size_t
    cdll.MagickGetImageDepth.argtypes = (MagickWand_p,)
    
    #resize
    cdll.MagickResizeImage.argtypes = (MagickWand_p, c_size_t, c_size_t, Filter, c_double)
    cdll.MagickResizeImage.restype = MagickBoolean
    
    #crop
    cdll.MagickCropImage.argtypes = (MagickWand_p, c_size_t, c_size_t, c_ssize_t, c_ssize_t)
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
    
    cdll.MagickForwardFourierTransformImage.argtypes = (MagickWand_p,)
    cdll.MagickForwardFourierTransformImage.restype = MagickBoolean
    
    cdll.MagickFxImage.argtypes = (MagickWand_p, c_char_p)
    cdll.MagickFxImage.restype = MagickWand_p
    
    cdll.MagickGammaImage.argtypes = (MagickWand_p, c_double)
    cdll.MagickGammaImage.restype = MagickBoolean

def guard(wand, callable, msg=None):
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
        