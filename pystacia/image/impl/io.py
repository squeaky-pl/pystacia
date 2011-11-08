def read_special(spec, width=None, height=None, factory=None):
    """Read special :term:`ImageMagick` image resource"""
    if not factory:
        factory = Image
        
    image = factory()
    
    resource = image.resource
    if width and height:
        guard(resource, lambda:
              cdll.MagickSetSize(resource, width, height))
    
    spec = b(spec)
    
    guard(resource, lambda: cdll.MagickReadImage(resource, spec))
    
    return image

from pystacia.image import Image