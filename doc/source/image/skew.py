from os.path import join, dirname

from pystacia import lena, axes

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)
image.skew(10, axes.x)
image.checkerboard()
image.write(join(dest, 'lena_skewx10.jpg'))
image.close()

image = lena(128)
image.skew(-5, axes.x)
image.checkerboard()
image.write(join(dest, 'lena_skewx-5.jpg'))
image.close()

image = lena(128)
image.skew(20, axes.y)
image.checkerboard()
image.write(join(dest, 'lena_skewy20.jpg'))
image.close()
