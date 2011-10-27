from tinyimg import lena

image = lena(128)
image.gamma(0.1)
image.write('../_static/generated/lena_gamma0.1.jpg')
image.close()

image = lena(128)
image.gamma(0.3)
image.write('../_static/generated/lena_gamma0.3.jpg')
image.close()

image = lena(128)
image.gamma(0.6)
image.write('../_static/generated/lena_gamma0.6.jpg')
image.close()

image = lena(128)
image.gamma(1.5)
image.write('../_static/generated/lena_gamma1.5.jpg')
image.close()

image = lena(128)
image.gamma(2)
image.write('../_static/generated/lena_gamma2.jpg')
image.close()