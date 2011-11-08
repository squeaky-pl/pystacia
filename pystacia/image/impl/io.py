def read_special(spec, width=None, height=None, factory=None):
    """Read special :term:`ImageMagick` image resource"""
    if not factory:
        factory = Image
        
    image = factory()
    
    if width and height:
        c_call('magick', 'set_size', image, width, height)
    
    c_call(image, 'read', spec)
    
    return image

from pystacia.image import Image
from pystacia.api.func import c_call