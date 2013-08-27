from os.path import dirname, join

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.denoise()
image.write(join(dest, 'lena_denoise.jpg'))
image.close()
