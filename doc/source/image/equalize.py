from pystacia import lena

image = lena(256)
image.equalize()
image.write('../_static/generated/lena_equalize.jpg')
image.close()