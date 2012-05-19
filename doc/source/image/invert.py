from pystacia import lena

image = lena(256)
image.invert()
image.write('../_static/generated/lena_invert.jpg')
image.close()
