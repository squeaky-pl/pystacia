def blur(image, radius, strength):
    if strength == None:
        strength = radius
    
    c_call(image, 'blur', radius, strength)

#TODO: moving center here
def radial_blur(image, angle):
    """Performs radial blur.
    
       :param angle: Blur angle in degrees
       :type angle: ``float``
       
       Radial blurs image within given angle.
       
       This method can be chained.
    """
    c_call(image, 'radial_blur', angle)

def denoise(image):
    """Attempt to remove noise preserving edges.
    
       Applies a digital filter that improves the quality of a
       noisy image.
       
       This method can be chained.
    """
    c_call(image, 'enhance')

def despeckle(image):
    """Attempt to remove speckle preserving edges.
       
       Resulting image almost solid color areas are smoothed preserving
       edges.
       
       This method can be chained.
    """
    c_call(image, 'despeckle')

def emboss(image, radius=0, strength=None):
    """Apply edge detecting algorithm.
       
       :param radius: filter radius
       :type radius: ``int``
       :param stregth: filter strength (sigma)
       :type strength: ``int``
       
       On a typical photo creates effect of raised edges.
       
       This method can be chained.
    """
    if strength == None:
        strength = radius
    
    c_call(image, 'emboss', radius, strength)


from pystacia.api.func import c_call