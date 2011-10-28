from tinyimg import lena

image = lena(256)
image.spread(2)
image.write('../_static/generated/lena_spread2.jpg')
image.close()

image = lena(256)
image.spread(6)
image.write('../_static/generated/lena_spread6.jpg')
image.close()