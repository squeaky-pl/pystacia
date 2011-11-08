def alloc(image):
    return simple_call('wand', 'new')
    
def free(image):
    return simple_call('wand', 'destroy', image)
    
def clone(image):
    return simple_call('wand', 'clone', image)

from pystacia.api.func import simple_call