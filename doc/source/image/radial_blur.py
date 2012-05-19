from pystacia import lena

image = lena(256)
image.radial_blur(10)
image.write('../_static/generated/lena_radial_blur10.jpg')
image.close()

image = lena(256)
image.radial_blur(45)
image.write('../_static/generated/lena_radial_blur45.jpg')
image.close()
