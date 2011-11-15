from pystacia.tests.common import TestCase
from pystacia.image import types, colorspaces


data = {
    'lena': {
        'size': (512, 512),
        'depth': 8,
        'type': types.truecolor,
        'colorspace': colorspaces.rgb
    },
    'magick_logo': {
        'size': (640, 480),
        'depth': 8,
        'type': types.palette,
        'colorspace': colorspaces.rgb
    },
    'netscape': {
        'size': (216, 144),
        'depth': 8,
        'type': types.palette,
        'colorspace': colorspaces.rgb
    },
    'rose': {
        'size': (70, 46),
        'depth': 8,
        'type': types.truecolor,
        'colorspace': colorspaces.rgb
    },
    'wizard': {
        'size': (480, 640),
        'depth': 8,
        'type': types.palette,
        'colorspace': colorspaces.rgb
    }
}


class SampleTest(TestCase):
    def test(self):
        if not lena_available():
            del data['lena']
            
        for sample, params in data.items():
            img = getattr(image, sample)()
            
            for param, value in params.items():
                self.assertEqual(getattr(img, param), value)
                
            img.close()


from pystacia import image
from pystacia.image.sample import lena_available
