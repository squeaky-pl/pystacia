from os.path import join, dirname

from pystacia import lena, axes

dest = join(dirname(__file__), '../_static/generated')

image = lena(128)
image.wave(20, 100)
image.checkerboard()
image.write(join(dest, 'lena_wave20,100,x.jpg'))
image.close()

image = lena(128)
image.wave(-10, 50)
image.checkerboard()
image.write(join(dest, 'lena_wave-10,50,x.jpg'))
image.close()

image = lena(128)
image.wave(50, 200, axis=axes.y)
image.checkerboard()
image.write(join(dest, 'lena_wave50,200,y.jpg'))
image.close()

image = lena(128)
image.wave(10, 30, axis=axes.y)
image.checkerboard()
image.write(join(dest, 'lena_wave10,30,y.jpg'))
image.close()
