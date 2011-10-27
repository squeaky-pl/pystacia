from tinyimg import lena

image = lena(256)
image.blur(3)
image.write('../_static/generated/lena_blur3.jpg')
image.close()

image = lena(256)
image.blur(10)
image.write('../_static/generated/lena_blur10.jpg')
image.close()