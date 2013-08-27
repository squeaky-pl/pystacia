from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.spread(2)
image.write(join(dest, 'lena_spread2.jpg'))
image.close()

image = lena(256)
image.spread(6)
image.write(join(dest, 'lena_spread6.jpg'))
image.close()
