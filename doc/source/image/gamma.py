from os.path import join, dirname

dest = join(dirname(__file__), '../_static/generated')

from pystacia import lena

image = lena(128)
image.gamma(0.1)
image.write(join(dest, 'lena_gamma0.1.jpg'))
image.close()

image = lena(128)
image.gamma(0.3)
image.write(join(dest, 'lena_gamma0.3.jpg'))
image.close()

image = lena(128)
image.gamma(0.6)
image.write(join(dest, 'lena_gamma0.6.jpg'))
image.close()

image = lena(128)
image.gamma(1.5)
image.write(join(dest, 'lena_gamma1.5.jpg'))
image.close()

image = lena(128)
image.gamma(2)
image.write(join(dest, 'lena_gamma2.jpg'))
image.close()
