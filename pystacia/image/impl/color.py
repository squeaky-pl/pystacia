def brightness(image, factor):
    c_call(image, 'brightness_contrast', factor * 100, 0)


def contrast(image, factor):
    c_call(image, 'brightness_contrast', 0, factor * 100)


def gamma(image, gamma):
    c_call(image, 'gamma', gamma)


def auto_gamma(image):
    c_call(image, 'auto_gamma')


def auto_level(image):
    c_call(image, 'auto_level')


def modulate(image, hue, saturation, lightness):
    c_call(image, 'modulate', lightness * 100 + 100, saturation * 100 + 100,
                              hue * 100 + 100)


from pystacia.api.func import c_call