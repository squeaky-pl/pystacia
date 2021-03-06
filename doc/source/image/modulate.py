from os.path import dirname, join

from pystacia import lena

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)
image.modulate(-1, -0.25, 0.1)
image.write(join(dest, 'lena_modulate-1,-0.25,0.1.jpg'))
image.close()

image = lena(128)
image.modulate(-0.5, 0.25, 0)
image.write(join(dest, 'lena_modulate-0.5,0.25,0.jpg'))
image.close()

image = lena(128)
image.modulate(-0.2, 0.5, -0.25)
image.write(join(dest, 'lena_modulate-0.2,0.5,-0.25.jpg'))
image.close()

image = lena(128)
image.modulate(0.4, -0.5, 0)
image.write(join(dest, 'lena_modulate0.4,-0.5,0.jpg'))
image.close()

image = lena(128)
image.modulate(0.8, 0, 0)
image.write(join(dest, 'lena_modulate0.8,0,0.jpg'))
image.close()
