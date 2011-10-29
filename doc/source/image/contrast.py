from pystacia import lena

image = lena(128)
image.contrast(-1)
image.write('../_static/generated/lena_contrast-1.jpg')
image.close()

image = lena(128)
image.contrast(-0.6)
image.write('../_static/generated/lena_contrast-0.6.jpg')
image.close()

image = lena(128)
image.contrast(-0.25)
image.write('../_static/generated/lena_contrast-0.25.jpg')
image.close()

image = lena(128)
image.contrast(0.25)
image.write('../_static/generated/lena_contrast0.25.jpg')
image.close()

image = lena(128)
image.contrast(1)
image.write('../_static/generated/lena_contrast1.jpg')
image.close()
