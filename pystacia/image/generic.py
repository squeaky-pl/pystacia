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


def noise(width, height, grayscale=False):
    """Create image filled with monolithic random noise
       
       :param width: Width in pixels
       :type width: ``int``
       :param height: Height in pixels
       :type height: ``int``
       :param grayscale: Whether noise should be grayscale
       
       By defult returns an image filled with color noise.
       The image contains grayscale noise if grayscale is set to ``True``.
    """
    
    image = blank(width, height, 'white')
    image.add_noise(noise_type='random')
    
    if grayscale:
        image.type = 'grayscale'
    
    return image


from pystacia.image._impl import io
from pystacia.api.func import call
