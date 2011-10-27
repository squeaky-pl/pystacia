from tinyimg import lena

image = lena(256)
image.sepia()
image.write('../_static/generated/lena_sepia.jpg')
image.close()