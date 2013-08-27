from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.rotate(5)
image2 = image.copy()
image.checkerboard()
image.write(join(dest, 'lena_notstraight.jpg'))
image.close()


image2.straighten(20)
image2.checkerboard()
image2.write(join(dest, 'lena_straightened.jpg'))
image2.close()
