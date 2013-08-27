from os.path import join, dirname

from pystacia import lena, color

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)
image.fill(color.from_string('red'))
image.write(join(dest, 'lena_fill_red.jpg'))
image.close()

image = lena(128)
image.fill(color.from_string('green'), 0.5)
image.write(join(dest, 'lena_fill_green.jpg'))
image.close()

image = lena(128)
image.fill(color.from_string('blue'), 0.25)
image.write(join(dest, 'lena_fill_blue.jpg'))
image.close()

image = lena(128)
image.fill(color.from_string('orange'), 0.2)
image.write(join(dest, 'lena_fill_orange.jpg'))
image.close()
