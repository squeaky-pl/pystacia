from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.emboss()
image.write(join(dest, 'lena_emboss.jpg'))
image.close()
