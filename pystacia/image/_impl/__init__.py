def alloc(image):
    return c_call('wand', 'new')


def free(image):
    return c_call('wand', 'destroy', image)


def clone(image):
    return c_call('wand', 'clone', image)


from pystacia.api.func import c_call
