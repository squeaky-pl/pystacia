#!/usr/bin/env python


from glob import glob
from os.path import dirname, abspath, join, basename, splitext, exists
from subprocess import check_call, check_output
from re import compile
from pprint import pprint


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


def reduce_(data):
    for key, values in data.items():
        print(key.upper() + '---------------------------')
        seen = {}
        for i, value in enumerate(values):
            copied = value.copy()
            version = copied.pop('_version')
            if copied == seen:
                values[i] = None
            else:
                print(' version ' + str(version))
                copied_set = set(copied.items())
                seen_set = set(seen.items())
                added = dict(copied_set - seen_set)
                removed = dict(seen_set - copied_set)

                if added:
                    print(' + ' + str(added))
                if removed:
                    print(' - ' + str(removed))

            seen = copied

        data[key] = filter(None, values)


min_version = (6, 5)


def main():
    downloads = join(here, 'downloads')
    archives = glob(join(downloads, '*.tar.bz2'))

    directories = []
    for archive in archives:
        directory, _ = splitext(splitext(archive)[0])

        version_str = basename(directory).split('-', 1)[1].replace('-', '.')
        version = tuple(int(v) for v in version_str.split('.'))
        if version < min_version:
            continue

        directories.append((version, directory))

        if exists(directory):
            continue

        print('Unpacking ' + basename(archive))
        check_call(['tar', '-C', downloads, '-xf', archive])

    data = dict((k, []) for k in enums)
    for version, directory in sorted(directories):
        result = process(directory)

        for name, values in result.items():
            values['_version'] = version[:-1]
            data[name].append(values)

    reduce_(data)

    with open(join(here, 'data.py'), 'w') as f:
        pprint(data, f)

    return data


if __name__ == '__main__':
    main()
