from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.sketch(3)
image.write(join(dest, 'lena_sketch3.jpg'))
image.close()

image = lena(256)
image.sketch(6, 0)
image.write(join(dest, 'lena_sketch6,0.jpg'))
image.close()
