from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.transpose()
image.write(join(dest, 'lena_transpose.jpg'))
image.close()

image = lena(256)
image.transverse()
image.write(join(dest, 'lena_transverse.jpg'))
image.close()
