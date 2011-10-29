from pystacia import lena, colorspaces


image = lena(256)

image.colorspace = colorspaces.ycbcr
image.write('../_static/generated/lena_ycbcr.jpg')

image.close()

image = lena(256)

image.colorspace = colorspaces.cmy
image.write('../_static/generated/lena_cmy.jpg')

image.close()