from tinyimg import lena

image = lena(256)
image.sketch(3)
image.write('../_static/generated/lena_sketch3.jpg')
image.close()

image = lena(256)
image.sketch(6, 0)
image.write('../_static/generated/lena_sketch6,0.jpg')
image.close()