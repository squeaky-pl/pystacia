from pystacia import lena

image = lena(256)

image.resize(128, 128)
image.write('../_static/generated/lena_resize1.jpg')

image.close()


image = lena(256)

image.resize(64, 128, 128, 128)
image.write('../_static/generated/lena_resize2.jpg')

image.close()
