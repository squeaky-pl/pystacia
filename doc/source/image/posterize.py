from os.path import dirname, join

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)
image.posterize(2)
image.write(join(dest, 'lena_posterize2.jpg'))
image.close()

image = lena(128)
image.posterize(3)
image.write(join(dest, 'lena_posterize3.jpg'))
image.close()

image = lena(128)
image.posterize(4)
image.write(join(dest, 'lena_posterize4.jpg'))
image.close()

image = lena(128)
image.posterize(5)
image.write(join(dest, 'lena_posterize5.jpg'))
image.close()
