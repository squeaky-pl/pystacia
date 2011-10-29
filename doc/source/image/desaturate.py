from pystacia import lena

image = lena(256)
image.desaturate()
image.write('../_static/generated/lena_desaturate.jpg')
image.close()
