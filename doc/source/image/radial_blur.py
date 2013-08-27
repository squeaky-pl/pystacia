from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.radial_blur(10)
image.write(join(dest, 'lena_radial_blur10.jpg'))
image.close()

image = lena(256)
image.radial_blur(45)
image.write(join(dest, 'lena_radial_blur45.jpg'))
image.close()
