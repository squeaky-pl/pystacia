#!/usr/bin/env python


from glob import glob
from os.path import dirname, abspath, join, basename, splitext, exists
from subprocess import check_call, check_output
from re import compile

here = dirname(abspath(__file__))
typedef_tmpl = 'typedef\s+enum\s*\{([^\}]+)\}\s*'
words = compile('([A-Z][a-z]*\d*)')


def split_by_word(value):
    return '_'.join(w.lower() for w in words.split(value) if w)


def compression(value):
    return 'lossless_jpeg' if value == 'LosslessJPEG' else value.lower()


def image_type(value):
    if value == 'TrueColor':
        return 'truecolor'
    elif value == 'TrueColorMatte':
        return 'truecolor_matte'
    else:
        return split_by_word(value)


enums = {
    'filter': ('FilterTypes', len('Filter'), split_by_word),
    'colorspace': ('ColorspaceType', len('Colorspace'), str.lower),
    'composite': ('CompositeOperator', len('CompositeOp'), split_by_word),
    'compression': ('CompressionType', len('Compression'), compression),
    'interpolation': ('InterpolatePixelMethod', len('InterpolatePixel'),
                      split_by_word),
    'metric': ('MetricType', len('Metric'), split_by_word),
    'noise': ('NoiseType', len('Noise'), split_by_word),
    'operation': ('MagickEvaluateOperator', len('EvaluateOpeartor'),
                  split_by_word),
    'type': ('ImageType', len('Type'), image_type),
}


def process(directory):
    preprocessed = check_output([
        'cpp', '-I', directory, join(directory, 'wand/MagickWand.h')])

    result = {}

    for enum, config in enums.items():
        c_name, ending, convert = config

        match = compile(typedef_tmpl + c_name).search(preprocessed)

        items = [v.strip() for v in match.groups()[0].split(',')]
        values = [i.split('=')[1].strip() if '=' in i else None for i in items]
        names = [convert(i.split('=')[0].strip()[:-ending]) for i in items]

        def filled():
            seen = -1

            for v in values:
                seen = int(v) if v else seen + 1
                yield seen

        if 'sentinel' in names:
            names.pop()
            values.pop()

        result[enum] = dict(zip(names, filled()))

    return result


def main():
    downloads = join(here, 'downloads')
    archives = glob(join(downloads, '*.tar.bz2'))

    directories = []
    for archive in archives:
        directory, _ = splitext(splitext(archive)[0])
        directories.append(directory)

        if exists(directory):
            continue

        print('Unpacking ' + basename(archive))
        check_call(['tar', '-C', downloads, '-xf', archive])

    for directory in directories:
        process(directory)

    return directories


if __name__ == '__main__':
    main()
