from os.path import join, dirname

from pystacia import lena, colorspaces

dest = join(dirname(__file__), '../_static/generated')

image = lena(256)

image.colorspace = colorspaces.ycbcr
image.write(join(dest, 'lena_ycbcr.jpg'))
image.close()

image = lena(256)

image.colorspace = colorspaces.cmy
image.write(join(dest, 'lena_cmy.jpg'))
image.close()
