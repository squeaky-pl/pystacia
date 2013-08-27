from os.path import join, dirname

from pystacia import blank, color, checkerboard

dest = join(dirname(__file__), '../_static/generated')

image = blank(100, 100)
image.checkerboard()
image.write(join(dest, 'transparent.jpg'))
image.close()

image = blank(100, 100, color.from_string('red'))
image.write(join(dest, 'red.jpg'))
image.close()

image = blank(100, 100, color.from_rgba(0, 1, 0, 0.5))
image.checkerboard()
image.write(join(dest, 'green.jpg'))
image.close()

image = checkerboard(200, 200)
image.write(join(dest, 'checkerboard.png'))
image.close()
