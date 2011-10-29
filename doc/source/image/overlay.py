from pystacia import lena, composites

overlay = lena(64)

image = lena(128)
image.overlay(overlay, 32, 32)
image.write('../_static/generated/lena_overlay1.jpg')
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.colorize)
image.write('../_static/generated/lena_overlay2.jpg')
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.multiply)
image.write('../_static/generated/lena_overlay3.jpg')
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.overlay)
image.write('../_static/generated/lena_overlay4.jpg')
image.close()


image = lena(128)
image.overlay(overlay, 32, 32, composites.pin_light)
image.write('../_static/generated/lena_overlay5.jpg')
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.saturate)
image.write('../_static/generated/lena_overlay6.jpg')
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.soft_light)
image.write('../_static/generated/lena_overlay7.jpg')
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.modulus_add)
image.write('../_static/generated/lena_overlay8.jpg')
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.modulus_subtract)
image.write('../_static/generated/lena_overlay9.jpg')
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.luminize)
image.write('../_static/generated/lena_overlay10.jpg')
image.close()

image = lena(128)
image.overlay(overlay, 32, 32, composites.hard_light)
image.write('../_static/generated/lena_overlay11.jpg')
image.close()