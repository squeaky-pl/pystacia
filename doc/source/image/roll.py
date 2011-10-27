from tinyimg import lena

image = lena(256)
image.roll(100, 0)
image.write('../_static/generated/lena_roll100_0.jpg')
image.close()

image = lena(256)
image.roll(-30, 40)
image.write('../_static/generated/lena_roll-30_40.jpg')
image.close()
