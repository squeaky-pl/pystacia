from pystacia import lena


image = lena(256)
image.transpose()
image.write('../_static/generated/lena_transpose.jpg')
image.close()

image = lena(256)
image.transverse()
image.write('../_static/generated/lena_transverse.jpg')
image.close()