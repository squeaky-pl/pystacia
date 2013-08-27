from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)

image.rotate(30)
image.checkerboard()
image.write(join(dest, 'lena_rotate30.jpg'))
image.close()


image = lena(128)

image.rotate(90)
image.write(join(dest, 'lena_rotate90.jpg'))
image.close()


image = lena(128)

image.rotate(-45)
image.checkerboard()
image.write(join(dest, 'lena_rotate-45.jpg'))
image.close()
