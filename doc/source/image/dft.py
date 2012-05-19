from pystacia import lena

image = lena(128)
images = image.dft()
images[0].write('../_static/generated/lena_magnitude.jpg')
images[1].write('../_static/generated/lena_phase.jpg')
image.close()

image = lena(128)
images = image.dft(False)
images[0].write('../_static/generated/lena_real.jpg')
images[1].write('../_static/generated/lena_imaginary.jpg')
image.close()
