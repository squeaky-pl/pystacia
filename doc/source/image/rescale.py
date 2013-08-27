from os.path import join, dirname

from pystacia import lena, filters

dest = join(dirname(__file__), '../_static/generated')

from all import closeup

image = lena()

image.rescale(256, 256)

image.write(join(dest, 'lena_rescale_256.jpg'))

image.rescale(100, 200)

image.write(join(dest, 'lena_rescale_300.jpg'))

image.rescale(128, 128)

image.write(join(dest, 'lena_rescale_128.jpg'))

image.close()


image = lena(256)

image.rescale(factor=0.75)

image.write(join(dest, 'lena_rescale_f0.75.jpg'))

image.rescale(factor=(0.6, 0.5))

image.write(join(dest, 'lena_rescale_f0.6_0.5.jpg'))

image.rescale(factor=(1.3, 1))

image.write(join(dest, 'lena_rescale_f1.3_1.jpg'))

image.close()

image = closeup(lambda i: i.rescale(factor=2, filter=filters.point), 2)

image.write(join(dest, 'lena_upscale_point.jpg'))

image.close()

image = closeup(lambda i: i.rescale(factor=2, filter=filters.cubic), 2)

image.write(join(dest, 'lena_upscale_cubic.jpg'))

image.close()

image = closeup(lambda i: i.rescale(factor=2, filter=filters.sinc), 2)

image.write(join(dest, 'lena_upscale_sinc.jpg'))

image.close()

image = closeup(lambda i: i.rescale(factor=2, filter=filters.lanczos), 2)

image.write(join(dest, 'lena_upscale_lanczos.jpg'))

image.close()

image = closeup(lambda i: i.rescale(factor=0.5, filter=filters.point))

image.write(join(dest, 'lena_downscale_point.jpg'))

image.close()

image = closeup(lambda i: i.rescale(factor=0.5, filter=filters.cubic))

image.write(join(dest, 'lena_downscale_cubic.jpg'))

image.close()

image = closeup(lambda i: i.rescale(factor=0.5, filter=filters.sinc))

image.write(join(dest, 'lena_downscale_sinc.jpg'))

image.close()

image = closeup(lambda i: i.rescale(factor=0.5, filter=filters.lanczos))

image.write(join(dest, 'lena_downscale_lanczos.jpg'))

image.close()
