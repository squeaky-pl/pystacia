from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)

image.resize(128, 128)
image.write(join(dest, 'lena_resize1.jpg'))
image.close()


image = lena(256)

image.resize(64, 128, 128, 128)
image.write(join(dest, 'lena_resize2.jpg'))
image.close()
