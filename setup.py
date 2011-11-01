# coding: utf-8
# setup.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

base_urls = [
    'https://bitbucket.org/liquibits/pystacia/downloads/'
]

magick_version = '6.7.3.2'

binaries = {
    'imagick-6.7.3.2-linux-i686.zip': '11f306efc9dacad6b4c39d32b8f4ea39',
    'imagick-6.7.3.2-linux-x86_64.zip': 'fd74668d2dc382eac7e26580a86ba0d0',
    'imagick-6.7.3.2-macosx-10.7-x86_64.zip': '4b9bde38265aa06bafee943b858f2237',
    'imagick-6.7.3.2-win32.zip': '7ac5ecd3357bcdb13c61d2b42a584823',
    'imagick-6.7.3.2-win-amd64.zip': '84eac45ee2697f03270d4743981aadc1'
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

from distutils.command.build import build


class pystacia_build(build):
    def run(self):
        result = build.run(self)
        
        local_file = join(self.build_base, 'lena.png')
        
        # download lena
        found = False
        for base in base_urls:
            url = base + 'lena.png'
            self.announce('==> Downloading: ' + url)
            urlretrieve(url, local_file)
            
            if md5_file(local_file) == lena_md5:
                self.announce('==> MD5 digest OK')
                found = True
                break
            
            self.warn('==> MD5 digest failed')
        
        if not found:
            self.warn('==> All the mirrors for lena.png failed')
        
        if environ.get('PYSTACIA_SKIP_BINARIES'):
            self.warn('==> Skipping binaries as requested')
            return result
        
        remote_file = ('imagick-' + magick_version + '-' +
                       pystacia_get_platform() + '.zip')
        
        if remote_file not in binaries:
            self.warn('==> Couldnt find binary Imagick for your platform')
            return result
        
        self.announce('==> Magick binary distribution: ' + remote_file)
        
        local_file = join(self.build_temp, remote_file)
        
        mkpath(self.build_temp)
        
        # download libraries
        found = False
        for base in base_urls:
            url = base + remote_file
            self.announce('==> Downloading: ' + url)
            urlretrieve(url, local_file)

            if md5_file(local_file) == binaries[remote_file]:
                self.announce('==> MD5 digest OK')
                found = True
                break
            
            self.warn('==> MD5 digest failed')
        
        if not found:
            self.warn('==> All the mirrors for libraries failed')
            return result
        
        lib_base = join(self.build_base, 'libraries')
        mkpath(lib_base)
        
        extract(local_file, lib_base)
        
        return result


from os.path import join, exists
from hashlib import md5
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve  # @Reimport
from zipfile import ZipFile

# patch ZipFile to have extract method, py25
if not hasattr(ZipFile, 'extract'):
    def zip_extract(z, name, path):
        f = open(join(path, name), 'wb')
        
        f.write(z.read(name))
        
        f.close()
        
    ZipFile.extract = zip_extract

from distutils.dir_util import mkpath
from distutils.util import get_platform

try:
    # this will be present with pip or setuptools was installed
    from setuptools.command.install import install
except ImportError:
    # still it can work with python setup.py install
    from distutils.command.install import install  # @Reimport


class pystacia_install(install):
    def run(self):
        result = install.run(self)
        
        lib_base = join(self.build_base, 'libraries')
        if exists(lib_base):
            self.copy_tree(lib_base, join(self.install_lib, 'pystacia/cdll'))
            
        lena = join(self.build_base, 'lena.png')
        if exists(lena):
            self.copy_file(lena, join(self.install_lib, 'pystacia/lena.png'))
            
        return result

install_requires = ['six', 'decorator']

try:
    format
except NameError:
    install_requires.append('StringFormat')

from os import environ
from setuptools import setup

packages = ['pystacia',
            'pystacia.tests',
            'pystacia.api',
            'pystacia.api.tests']

cmdclass = dict(build=pystacia_build,
                install=pystacia_install)

setup(
    name='pystacia',
    description='Python raster imaging library',
    author='Paweł Piotr Przeradowski',
    author_email='przeradowski@gmail.com',
    url='http://liquibits.bitbucket.org/',
    version='0.1beta',
    packages=packages,
    license='MIT License',
    long_description=open('README').read(),
    install_requires=install_requires,
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
          'Programming Language :: Python :: 3',
          'Topic :: Multimedia :: Graphics',
    ],
)
