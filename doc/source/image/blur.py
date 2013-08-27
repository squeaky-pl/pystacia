from os.path import dirname, join

from pystacia import lena


dest = join(dirname(__file__), '../_static/generated')


image = lena(256)
image.blur(3)
image.write(join(dest, 'lena_blur3.jpg'))
image.close()

image = lena(256)
image.blur(10)
image.write(join(dest, 'lena_blur10.jpg'))
image.close()
