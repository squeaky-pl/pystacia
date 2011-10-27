from tinyimg import lena

image = lena(256)
image.swirl(60)
image.write('../_static/generated/lena_swirl60.jpg')
image.close()

image = lena(256)
image.swirl(-30)
image.write('../_static/generated/lena_swirl-30.jpg')
image.close()
