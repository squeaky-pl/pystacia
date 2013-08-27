from os.path import dirname, join

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.oil_paint(3)
image.write(join(dest, 'lena_oil_paint3.jpg'))
image.close()

image = lena(256)
image.oil_paint(8)
image.write(join(dest, 'lena_oil_paint8.jpg'))
image.close()
