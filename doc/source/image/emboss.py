from pystacia import lena

image = lena(256)
image.emboss()
image.write('../_static/generated/lena_emboss.jpg')
image.close()