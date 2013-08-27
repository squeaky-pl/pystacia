from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.sepia()
image.write(join(dest, 'lena_sepia.jpg'))
image.close()
