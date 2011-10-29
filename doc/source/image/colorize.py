from pystacia import lena,  color

image = lena(128)
image.colorize(color.from_string('red'))
image.write('../_static/generated/lena_colorize_red.jpg')
image.close()

image = lena(128)
image.colorize(color.from_string('yellow'))
image.write('../_static/generated/lena_colorize_yellow.jpg')
image.close()

image = lena(128)
image.colorize(color.from_string('blue'))
image.write('../_static/generated/lena_colorize_blue.jpg')
image.close()

image = lena(128)
image.colorize(color.from_string('violet'))
image.write('../_static/generated/lena_colorize_violet.jpg')
image.close()