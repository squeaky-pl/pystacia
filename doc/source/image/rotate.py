from tinyimg import lena

image = lena(128)

image.rotate(30)
image.checkerboard()
image.write('../_static/generated/lena_rotate30.jpg')

image.close()


image = lena(128)

image.rotate(90)
image.write('../_static/generated/lena_rotate90.jpg')

image.close()


image = lena(128)

image.rotate(-45)
image.checkerboard()
image.write('../_static/generated/lena_rotate-45.jpg')

image.close()