def alloc(color):
    return simple_call('pwand', 'new')

def free(color):
    return simple_call('pwand', 'destroy', color)

def clone(color):
    return simple_call('pwand', 'destroy', color)


def get_red(color):
    return saturate(c_call(color, 'get_red'))


def set_red(color, value):
    c_call(color, 'set_red', value)


def get_green(color):
    return saturate(c_call(color, 'get_green'))


def set_green(color, value):
    c_call(color, 'set_green', value)


def get_blue(color):
    return saturate(c_call(color, 'get_blue'))


def set_blue(color, value):
    c_call(color, 'set_blue', value)


def get_alpha(color):
    return saturate(c_call(color, 'get_alpha'))


def set_alpha(color, value):
    c_call(color, 'set_alpha', value)


def saturate(v):
    if v == 0:
        return 0
    elif v == 1:
        return 1
    else:
        return round(v, 4)

from pystacia.api.func import simple_call, c_call