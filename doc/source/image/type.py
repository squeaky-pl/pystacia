from os.path import join, dirname

from pystacia import types

dest = join(dirname(__file__), '../_static/generated')

from all import closeup


def palette(i):
    i.type = types.palette

image = closeup(palette)

image.write(join(dest, 'lena_palette.png'))

image.close()


def grayscale(i):
    i.type = types.grayscale

image = closeup(grayscale)

image.write(join(dest, 'lena_gray.jpg'))

image.close()


def bilevel(i):
    i.type = types.bilevel

image = closeup(bilevel)

image.write(join(dest, 'lena_bilevel.png'))

image.close()
