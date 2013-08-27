from os.path import join, dirname

from pystacia import lena, axes

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)

image.flip(axes.x)
image.write(join(dest, 'lena_flipx.jpg'))
image.close()


image = lena(256)

image.flip(axes.y)
image.write(join(dest, 'lena_flipy.jpg'))
image.close()
