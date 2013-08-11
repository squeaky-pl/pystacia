#!/usr/bin/env python


from urllib2 import urlopen
from re import compile
from os.path import join, exists, basename, abspath, dirname
from os import mkdir
from os import errno
from subprocess import check_call


href = compile('href\s*=\s*[\'"]([^\'"]+)')


def find_links(index):
    links = []

    f = urlopen(index)

    content = f.read()

    for link in href.findall(content):
        if link.startswith('ImageMagick-') and link.endswith('.tar.bz2'):
            links.append(join(index, link))

    f.close()

    return links


def main():
    links = (find_links('http://www.imagemagick.org/download/')
             + find_links('http://www.imagemagick.org/download/legacy/'))

    here = dirname(abspath(__file__))
    downloads = join(here, 'downloads')

    try:
        mkdir(downloads)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for link in links:
        dest = join(downloads, basename(link))
        if not exists(dest):
            check_call(['wget', '-O', dest, link])

    return links


if __name__ == '__main__':
    main()
