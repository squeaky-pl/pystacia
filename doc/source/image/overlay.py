from os.path import join, dirname

from pystacia import lena, composites

dest = join(dirname(__file__), '../_static/generated')

overlay = lena(64)

image = lena(128)
image.overlay(overlay, 32, 32)
image.write(join(dest, 'lena_overlay1.jpg'))
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.colorize)
image.write(join(dest, 'lena_overlay2.jpg'))
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.multiply)
image.write(join(dest, 'lena_overlay3.jpg'))
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.overlay)
image.write(join(dest, 'lena_overlay4.jpg'))
image.close()


image = lena(128)
image.overlay(overlay, 32, 32, composites.pin_light)
image.write(join(dest, 'lena_overlay5.jpg'))
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.saturate)
image.write(join(dest, 'lena_overlay6.jpg'))
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.soft_light)
image.write(join(dest, 'lena_overlay7.jpg'))
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.modulus_add)
image.write(join(dest, 'lena_overlay8.jpg'))
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.modulus_subtract)
image.write(join(dest, 'lena_overlay9.jpg'))
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.luminize)
image.write(join(dest, 'lena_overlay10.jpg'))
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.hard_light)
image.write(join(dest, 'lena_overlay11.jpg'))
image.close()
