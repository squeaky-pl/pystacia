from pystacia import lena

image = lena(256)
image.rotate(5)
image.straighten(20)
image2 = image.copy()
image.checkerboard()
image.write('../_static/generated/lena_extrabg.jpg')
image.close()

image2.trim()
image2.write('../_static/generated/lena_trim.jpg')
image2.close()
