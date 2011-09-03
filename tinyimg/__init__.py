from sys import argv
import atexit
from ctypes import CDLL
from ctypes.util import find_library

from .func import annote

def init():
    global cdll
    cdll = CDLL(find_library('magickCore'))
    
    annote(cdll)
    
    if not cdll.IsMagickInstantiated():
        cdll.MagickCoreGenesis(argv[0], True)
        
        def _atexit():
            if cdll.IsMagickInstantiated(): cdll.MagickCoreTerminus()
        
        atexit.register(_atexit)
    
class Image(object):
    def __init__(self):
        pass
    
init()

__all__ = [Image]