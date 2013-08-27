from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)
image.set_alpha(0.75)
image.checkerboard()
image.write(join(dest, 'lena_alpha0.75.jpg'))
image.close()

image = lena(128)
image.set_alpha(0.5)
image.checkerboard()
image.write(join(dest, 'lena_alpha0.5.jpg'))
image.close()

image = lena(128)
image.set_alpha(0.25)
image.checkerboard()
image.write(join(dest, 'lena_alpha0.25.jpg'))
image.close()

image = lena(128)
image.set_alpha(0)
image.checkerboard()
image.write(join(dest, 'lena_alpha0.jpg'))
image.close()
