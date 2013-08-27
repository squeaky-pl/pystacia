from os.path import dirname, join

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)
image.contrast(-1)
image.write(join(dest, 'lena_contrast-1.jpg'))
image.close()

image = lena(128)
image.contrast(-0.6)
image.write(join(dest, 'lena_contrast-0.6.jpg'))
image.close()

image = lena(128)
image.contrast(-0.25)
image.write(join(dest, 'lena_contrast-0.25.jpg'))
image.close()

image = lena(128)
image.contrast(0.25)
image.write(join(dest, 'lena_contrast0.25.jpg'))
image.close()

image = lena(128)
image.contrast(1)
image.write(join(dest, 'lena_contrast1.jpg'))
image.close()
