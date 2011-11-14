def checkerboard(width, height, factory=None):
    """Returns standard checkerboard image
      
       :param width: width  in pixels
       :type width: ``int``
       :param height: height in pixels
       :type height: ``int``
       :rtype: :class:`pystacia.image.Image` or factory
    """
    return call(io.read, 'pattern:checkerboard',
                                width, height, factory)


def blank(width, height, background=None, factory=None):
    """Create :class:`Image` with monolithic background
       
       :param width: Width in pixels
       :type width: ``int``
       :param height: Height in pixels
       :type height: ``int``
       :param background: background color, defaults to fully transparent
       :type background: :class:`pystacia.Color`
       
       Creates blank image of given dimensions filled with background color.
       
       >>> blank(32, 32, color.from_string('red'))
       <Image(w=32,h=32,16bit,rgb,palette) object at 0x108006000L>
    """
    if not background:
        background = 'transparent'
    
    return call(io.read, 'xc:' + str(background),
                width, height, factory)
    
from pystacia.image._impl import io
from pystacia.api.func import call
