from pystacia import lena

image = lena(256)
image.oil_paint(3)
image.write('../_static/generated/lena_oil_paint3.jpg')
image.close()

image = lena(256)
image.oil_paint(8)
image.write('../_static/generated/lena_oil_paint8.jpg')
image.close()