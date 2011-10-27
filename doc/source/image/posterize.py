from tinyimg import lena

image = lena(128)
image.posterize(2)
image.write('../_static/generated/lena_posterize2.jpg')
image.close()

image = lena(128)
image.posterize(3)
image.write('../_static/generated/lena_posterize3.jpg')
image.close()

image = lena(128)
image.posterize(4)
image.write('../_static/generated/lena_posterize4.jpg')
image.close()

image = lena(128)
image.posterize(5)
image.write('../_static/generated/lena_posterize5.jpg')
image.close()