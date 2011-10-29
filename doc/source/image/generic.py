from tinyimg import blank, color, checkerboard

image = blank(100, 100)
image.checkerboard()
image.write('../_static/generated/transparent.jpg')
image.close()

image = blank(100, 100, color.from_string('red'))
image.write('../_static/generated/red.jpg')
image.close()

image = blank(100, 100, color.from_rgba(0, 1, 0, 0.5))
image.checkerboard()
image.write('../_static/generated/green.jpg')
image.close()

image = checkerboard(200, 200)
image.write('../_static/generated/checkerboard.png')
image.close()