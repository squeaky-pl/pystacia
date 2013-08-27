from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.equalize()
image.write(join(dest, 'lena_equalize.jpg'))
image.close()
