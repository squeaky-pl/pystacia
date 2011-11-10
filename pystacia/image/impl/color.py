def brightness(image, factor):
    c_call(image, 'brightness_contrast', factor * 100, 0)


def contrast(image, factor):
    c_call(image, 'brightness_contrast', 0, factor * 100)


def gamma(image, gamma):
    c_call(image, 'gamma', gamma)


def auto_gamma(image):
    c_call(image, 'auto_gamma')


from pystacia.api.func import c_call