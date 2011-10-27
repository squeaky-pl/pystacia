from tinyimg import lena, axes


image = lena(128)
image.skew(10, axes.x)
image.checkerboard()
image.write('../_static/generated/lena_skewx10.jpg')
image.close()

image = lena(128)
image.skew(-5, axes.x)
image.checkerboard()
image.write('../_static/generated/lena_skewx-5.jpg')
image.close()

image = lena(128)
image.skew(20, axes.y)
image.checkerboard()
image.write('../_static/generated/lena_skewy20.jpg')
image.close()