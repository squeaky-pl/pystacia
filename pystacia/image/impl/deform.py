def swirl(image, angle):
    c_call(image, 'swirl', angle)


def wave(image, amplitude, length, offset, axis):
    if not axis:
        axis = axes.x
        
    transparent = from_string('transparent')
    
    # preserve background color
    old_color = Color()

    c_call(image, ('get', 'background_color'), old_color)
    c_call(image, ('set', 'background_color'), transparent)
    
    c_call(image, 'wave', amplitude, length)
    
    c_call(image, ('set', 'background_color'), old_color)


from pystacia.api.func import c_call
from pystacia.color import from_string, Color
from pystacia.image import axes
