from pystacia import lena 

image = lena(256)
image.fx('u * 1/2')
image.write('../_static/generated/lena_fx.jpg')
image.close()