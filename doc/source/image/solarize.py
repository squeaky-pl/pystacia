from pystacia import lena

image = lena(256)
image.solarize(0.5)
image.write('../_static/generated/lena_solarize0.5.jpg')
image.close()

image = lena(256)
image.solarize(1)
image.write('../_static/generated/lena_solarize1.jpg')
image.close()