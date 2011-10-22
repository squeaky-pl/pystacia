# coding: utf-8

base_urls = [
    'https://bitbucket.org/squeaky/tinyimg/downloads/'
]

magick_version = '6.7.2.10'

binaries = {
    'imagick-6.7.2.10-win32.zip': '1a9e7c9514fde117737de4f7e730db40'
}

def md5_file(f, block_size=1**20):
    fingerprint = md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        fingerprint.update(data)
    return fingerprint.hexdigest()

def extract(zipfile, path):
    z = ZipFile(zipfile)
    for name in z.namelist():
        z.extract(name, path)
    z.close()

from distutils.command.build import build

class tinyimg_build(build):
    def run(self):
        result = build.run(self)
        
        remote_file = ('imagick-' + magick_version + '-' +
                       get_platform() + '.zip')
        
        if remote_file not in binaries:
            return result
        
        self.announce('==> Magick binary distribution: ' + remote_file)
        
        local_file = join(self.buile_temp, remote_file)
        
        mkpath(self.build_temp)
        
        found = False
        for base in base_urls:
            url = base + remote_file
            self.announce('==> Downloading: ' + url)
            urlretrieve(url, local_file)
            if md5_file(local_file) == binaries[remote_file][1]:
                self.announce('==> MD5 digest OK')
                found = True
                break
            
            self.announce('==> MD5 digest failed')
        
        if not found:
            return result
        
        lib_base = join(self.build_base, 'libraries')
        mkpath(lib_base)
        
        extract(local_file, lib_base)
        
        return result


from os.path import join 
from hashlib import md5
from urllib import urlretrieve
from zipfile import ZipFile

from distutils.dir_util import mkpath
from distutils.util import get_platform

try:
    # this will be present with pip or setuptools was installed
    from setuptools.command.install import install
except ImportError:
    # still it can work with python setup.py install
    from distutils.command.install import install

class tinyimg_install(install):
    def run(self):
        from os.path import join 
        
        result = install.run(self)
        
        lib_base = join(self.build_base, 'libraries')
        self.copy_tree(lib_base, join(self.install_lib, 'tinyimg/lib'))
        
        return result

install_requires=['six', 'decorator']

try:
    format
except NameError:
    install_requires.append('StringFormat')


from setuptools import setup

setup(
    name='tinyimg',
    description='Python raster imaging library',
    author='Paweł Piotr Przeradowski',
    author_email = 'przeradowski@gmail.com',
    url='https://bitbucket.org/squeaky/tinyimg',
    version='0.1dev',
    packages=['tinyimg', 'tinyimg.api', 'tinyimg.tests', 'tinyimg.api.tests'],
    package_data={'tinyimg': ['lena.ycbcr.bz2']},
    license='MIT License',
    long_description=open('README').read(),
    install_requires=install_requires,
    cmdclass=dict(build=tinyimg_build,
                  install=tinyimg_install)
)
