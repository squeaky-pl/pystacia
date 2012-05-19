from pystacia import types

from all import closeup


def palette(i):
    i.type = types.palette

image = closeup(palette)

image.write('../_static/generated/lena_palette.png')

image.close()


def grayscale(i):
    i.type = types.grayscale

image = closeup(grayscale)

image.write('../_static/generated/lena_gray.jpg')

image.close()


def bilevel(i):
    i.type = types.bilevel

image = closeup(bilevel)

image.write('../_static/generated/lena_bilevel.png')

image.close()
