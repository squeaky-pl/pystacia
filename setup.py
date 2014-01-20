# coding: utf-8

# setup.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski

# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from ez_setup import use_setuptools
use_setuptools()


from os import makedirs, remove, environ
from os.path import exists, join, abspath, dirname
from tempfile import gettempdir
from hashlib import md5
from shutil import rmtree
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve  # @Reimport
from zipfile import ZipFile
from distutils.dir_util import mkpath
from distutils.util import get_platform
from setuptools.command.install import install
from distutils.command.build import build
from setuptools import setup
from sys import version_info


if version_info < (2, 5):
    raise NotImplementedError(
        "Sorry, you need at least Python 2.5 or Python 3.x")


environ['PYSTACIA_SETUP'] = '1'
import pystacia


cache_dir = join(gettempdir(), 'pystacia', pystacia.__version__)

mirrors = [
    'https://bitbucket.org/liquibits/pystacia/downloads/'
]

magick_version = '6.7.3.2'

binaries = {
    'imagick-6.7.3.2-linux-i686.zip':
    '11f306efc9dacad6b4c39d32b8f4ea39',

    'imagick-6.7.3.2-linux-x86_64.zip':
    'fd74668d2dc382eac7e26580a86ba0d0',

    'imagick-6.7.3.2-macosx-10.7-x86_64.zip':
    '4b9bde38265aa06bafee943b858f2237',

    'imagick-6.7.3.2-win32.zip':
    '7ac5ecd3357bcdb13c61d2b42a584823',

    'imagick-6.7.3.2-win-amd64.zip':
    '84eac45ee2697f03270d4743981aadc1'
}


def pystacia_get_platform():
    platform = get_platform()

    renames = {'macosx-10.6-intel': 'macosx-10.7-x86_64'}

    try:
        platform = renames[platform]
    except KeyError:
        pass

    return platform

lena_md5 = '525f53c89dbfaa81a9c94e5bf7e1c7fd'


def md5_file(f, block_size=1 ** 20):
    f = open(f, 'rb')
    fingerprint = md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        fingerprint.update(data)
    f.close()

    return fingerprint.hexdigest()


def extract(zipfile, path):
    z = ZipFile(zipfile)
    for name in z.namelist():
        z.extract(name, path)
    z.close()


def download(build, mirrors, dest, filename, checksum):
    dest_file = join(dest, filename)

    if exists(dest_file):
        if md5_file(dest_file) == checksum:
            # we already have it in the cache
            build.announce('==> Cached ' + filename + ' MD5 digest OK')
            return dest_file
        else:
            remove(dest_file)
            build.warn('==> Cached ' + filename + ' MD5 digest failed')

    # download lena
    for mirror in mirrors:
        url = mirror + filename
        build.announce('==> Downloading: ' + url)
        urlretrieve(url, dest_file)

        if md5_file(dest_file) == checksum:
            build.announce('==> MD5 digest' + filename + ' OK')
            return dest_file

        build.warn('==> MD5 digest ' + filename + ' failed')

    build.warn('==> All the mirrors for ' + filename + ' failed')

    return False


class pystacia_build(build):
    def run(self):
        result = build.run(self)

        if not exists(cache_dir):
            makedirs(cache_dir)

        download(self, mirrors, cache_dir, 'lena.png', lena_md5)

        if environ.get('PYSTACIA_SKIP_BINARIES'):
            self.warn('==> Skipping binaries as requested')
            return result

        filename = ('imagick-' + magick_version + '-' +
                    pystacia_get_platform() + '.zip')

        if filename not in binaries:
            self.warn('==> Couldnt find binary Imagick for your platform')
            return result

        self.announce('==> Magick binary distribution: ' + filename)

        if not download(self, mirrors, cache_dir, filename,
                        binaries[filename]):
            return result

        lib_base = join(cache_dir, 'libraries')
        if exists(lib_base):
            rmtree(lib_base)

        mkpath(lib_base)

        extract(join(cache_dir, filename), lib_base)

        return result


# patch ZipFile to have extract method, py25
if not hasattr(ZipFile, 'extract'):
    def zip_extract(z, name, path):
        f = open(join(path, name), 'wb')

        f.write(z.read(name))

        f.close()

    ZipFile.extract = zip_extract


class pystacia_install(install):
    def run(self):
        result = install.run(self)

        lib_base = join(cache_dir, 'libraries')
        if exists(lib_base):
            self.copy_tree(lib_base, join(self.install_lib, 'pystacia/cdll'))

        lena = join(cache_dir, 'lena.png')
        if exists(lena):
            self.copy_file(lena, join(self.install_lib, 'pystacia/lena.png'))

        return result

install_requires = ['six', 'decorator', 'zope.deprecation']

try:
    format
except NameError:
    install_requires.append('StringFormat')

packages = ['pystacia',
            'pystacia.api',
            'pystacia.api.tests',
            'pystacia.color',
            'pystacia.image',
            'pystacia.image._impl',
            'pystacia.image.tests',
            'pystacia.magick',
            'pystacia.tests']

cmdclass = dict(build=pystacia_build,
                install=pystacia_install)


readme = open(join(dirname(abspath(__file__)), 'README.rst'))
long_description = readme.read()
readme.close()

test_require = ['nose', 'coverage']
if version_info < (2, 7):
    test_require.append('unittest2')

travis_require = test_require + ['coveralls']

docs_require = ['sphinx']

dev_require = test_require + docs_require + ['ipython']

lint_require = ['pylama', 'pylint', 'py3kwarn', 'clonedigger', 'html2rest']

setup(
    name='pystacia',
    description='Python raster imaging library',
    author=pystacia.__author__,  # Paweł Piotr Przeradowski
    author_email='przeradowski@gmail.com',
    url='http://liquibits.bitbucket.org/',
    version=pystacia.__version__,
    packages=packages,
    license='MIT License',
    long_description=long_description,
    install_requires=install_requires,
    extras_require={
        'test': test_require,
        'travis': travis_require,
        'lint': lint_require,
        'docs': docs_require,
        'dev': dev_require,
        'lint': lint_require
    },
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Graphics',
    ],
)
