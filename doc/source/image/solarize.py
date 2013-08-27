from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.solarize(0.5)
image.write(join(dest, 'lena_solarize0.5.jpg'))
image.close()

image = lena(256)
image.solarize(1)
image.write(join(dest, 'lena_solarize1.jpg'))
image.close()
