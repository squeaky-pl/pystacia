from tinyimg import lena

image = lena(256)
image.rotate(5)
image2 = image.copy()
image.checkerboard()
image.write('../_static/generated/lena_notstraight.jpg')
image.close()


image2.straighten(20)
image2.checkerboard()
image2.write('../_static/generated/lena_straightened.jpg')
image2.close()