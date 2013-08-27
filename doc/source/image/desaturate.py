from os.path import dirname, join

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.desaturate()
image.write(join(dest, 'lena_desaturate.jpg'))
image.close()
