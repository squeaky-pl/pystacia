from os.path import dirname, join

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)
image.brightness(-1)
image.write(join(dest, 'lena_brightness-1.jpg'))
image.close()

image = lena(128)
image.brightness(-0.6)
image.write(join(dest, 'lena_brightness-0.6.jpg'))
image.close()

image = lena(128)
image.brightness(-0.25)
image.write(join(dest, 'lena_brightness-0.25.jpg'))
image.close()

image = lena(128)
image.brightness(0.25)
image.write(join(dest, 'lena_brightness0.25.jpg'))
image.close()

image = lena(128)
image.brightness(0.75)
image.write(join(dest, 'lena_brightness0.75.jpg'))
image.close()
