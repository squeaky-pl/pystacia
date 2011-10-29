from pystacia import lena, color

image = lena(128)
image.set_color(color.from_string('red'))
image.write('../_static/generated/lena_set_color_red.jpg')
image.close()

image = lena(128)
image.set_color(color.from_rgba(0, 1, 0, 0.5))
image.checkerboard()
image.write('../_static/generated/lena_set_color_green.jpg')
image.close()

image = lena(128)
image.set_color(color.from_rgba(0, 0, 0, 0.2))
image.checkerboard()
image.write('../_static/generated/lena_set_color_black.jpg')
image.close()

image = lena(128)
image.set_color(color.from_rgba(1, 0, 1, 0.5))
image.checkerboard()
image.write('../_static/generated/lena_set_color_violet.jpg')
image.close()