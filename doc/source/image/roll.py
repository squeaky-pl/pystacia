from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.roll(100, 0)
image.write(join(dest, 'lena_roll100_0.jpg'))
image.close()

image = lena(256)
image.roll(-30, 40)
image.write(join(dest, 'lena_roll-30_40.jpg'))
image.close()
