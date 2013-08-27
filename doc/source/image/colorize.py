from os.path import dirname, join

from pystacia import lena,  color

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)
image.colorize(color.from_string('red'))
image.write(join(dest, 'lena_colorize_red.jpg'))
image.close()

image = lena(128)
image.colorize(color.from_string('yellow'))
image.write(join(dest, 'lena_colorize_yellow.jpg'))
image.close()

image = lena(128)
image.colorize(color.from_string('blue'))
image.write(join(dest, 'lena_colorize_blue.jpg'))
image.close()

image = lena(128)
image.colorize(color.from_string('violet'))
image.write(join(dest, 'lena_colorize_violet.jpg'))
image.close()
