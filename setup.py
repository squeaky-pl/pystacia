# coding: utf-8

from distutils.core import setup
from distutils.command.install import install

class tinyimg_install(install):
    def run(self):
        install.run(self)
        
        print('==> Installing binary ImageMagick distribution')

install_requires=['six', 'decorator']

try: format
except NameError:
    install_requires.append('StringFormat')

setup(
    name='tinyimg',
    description='Python raster imaging library',
    author = 'Paweł Piotr Przeradowski',
    author_email = 'przeradowski@gmail.com',
    url = 'https://bitbucket.org/squeaky/tinyimg',
    version='0.1dev',
    packages=['tinyimg', 'tinyimg.api', 'tinyimg.tests', 'tinyimg.api.tests'],
    package_data={'tinyimg': ['lena.ycbcr.bz2']},
    license='MIT License',
    long_description=open('README').read(),
    install_requires=install_requires,
    cmdclass=dict(install=tinyimg_install)
)
