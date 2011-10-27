from tinyimg import lena

image = lena(256)
image.denoise()
image.write('../_static/generated/lena_denoise.jpg')
image.close()