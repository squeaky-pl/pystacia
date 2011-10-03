# coding: utf-8

from distutils.core import setup

setup(
    name='tinyimg',
    description='Python raster imaging library',
    author = 'Paweł Piotr Przeradowski',
    author_email = 'przeradowski@gmail.com',
    url = 'https://bitbucket.org/squeaky/tinyimg',
    version='0.1dev',
    packages=['tinyimg', 'tinyimg.api', 'tinyimg.tests', 'tinyimg.api.tests'],
    license='MIT License',
    long_description=open('README').read(),
)