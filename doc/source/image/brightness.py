from pystacia import lena

image = lena(128)
image.brightness(-1)
image.write('../_static/generated/lena_brightness-1.jpg')
image.close()

image = lena(128)
image.brightness(-0.6)
image.write('../_static/generated/lena_brightness-0.6.jpg')
image.close()

image = lena(128)
image.brightness(-0.25)
image.write('../_static/generated/lena_brightness-0.25.jpg')
image.close()

image = lena(128)
image.brightness(0.25)
image.write('../_static/generated/lena_brightness0.25.jpg')
image.close()

image = lena(128)
image.brightness(0.75)
image.write('../_static/generated/lena_brightness0.75.jpg')
image.close()
