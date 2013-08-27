from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.fx('u * 1/2')
image.write(join(dest, 'lena_fx.jpg'))
image.close()
