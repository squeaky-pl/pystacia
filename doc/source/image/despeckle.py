from pystacia import lena

image = lena(256)
image.despeckle()
image.write('../_static/generated/lena_despeckle.jpg')
image.close()