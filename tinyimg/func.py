from ctypes import c_char_p

from .types import MagickWand_p, MagickBoolean

def annote(cdll):
    cdll.MagickWandGenesis.restype = None
    cdll.MagickWandGenesis.argtypes = ()
    
    cdll.MagickWandTerminus.argtypes = ()
    cdll.MagickWandTerminus.restype = None
    
    #wand
    cdll.NewMagickWand.restype = MagickWand_p
    cdll.NewMagickWand.argtypes = ()
    
    cdll.DestroyMagickWand.restype = MagickWand_p
    cdll.DestroyMagickWand.argtypes = (MagickWand_p,)
    
    #reading
    cdll.MagickReadImage.restype = MagickBoolean
    cdll.MagickReadImage.argtypes = (MagickWand_p, c_char_p)

