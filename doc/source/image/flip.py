from pystacia import lena, axes

image = lena(256)

image.flip(axes.x)
image.write('../_static/generated/lena_flipx.jpg')

image.close()


image = lena(256)

image.flip(axes.y)
image.write('../_static/generated/lena_flipy.jpg')

image.close()