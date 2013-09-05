from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.rotate(5)
image.straighten(20)
image2 = image.copy()
image.checkerboard()
image.write(join(dest, 'lena_extrabg.jpg'))
image.close()

image2.trim()
image2.write(join(dest, 'lena_trim.jpg'))
image2.close()
