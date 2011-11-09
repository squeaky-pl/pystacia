def alloc(color):
    return simple_call('pwand', 'new')

def free(color):
    return simple_call('pwand', 'destroy', color)

def clone(color):
    return simple_call('pwand', 'destroy', color)

from pystacia.api.func import simple_call