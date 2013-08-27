from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.swirl(60)
image.write(join(dest, 'lena_swirl60.jpg'))
image.close()

image = lena(256)
image.swirl(-30)
image.write(join(dest, 'lena_swirl-30.jpg'))
image.close()
