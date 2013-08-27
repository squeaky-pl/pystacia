from os.path import join, dirname

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)
image.despeckle()
image.write(join(dest, 'lena_despeckle.jpg'))
image.close()
