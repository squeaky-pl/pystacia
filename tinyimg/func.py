from ctypes import c_char_p

from struct import MagickBoolean

def annote(cdll):
    cdll.IsMagickInstantiated.restype = MagickBoolean
    cdll.IsMagickInstantiated.argtypes = ()
    
    cdll.MagickCoreGenesis.restype = MagickBoolean
    cdll.MagickCoreGenesis.argtypes = (c_char_p, MagickBoolean)
    
    cdll.MagickCoreTerminus.argtypes = ()
    cdll.MagickCoreTerminus.restype = None

