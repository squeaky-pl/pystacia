# coding: utf-8

def extract(zipfile, path):
    from zipfile import ZipFile
    z = ZipFile(zipfile)
    for name in z.namelist():
        z.extract(name, path)
    z.close()

from distutils.command.build import build

class tinyimg_build(build):
    def run(self):
        result = build.run(self)
        
        from os.path import join 
        from distutils.file_util import write_file
        from distutils.dir_util import mkpath
        from urllib import urlretrieve

        lib_base = join(self.build_base, 'libraries')
        mkpath(lib_base)
	mkpath(self.build_temp)
        urlretrieve('https://bitbucket.org/squeaky/tinyimg/downloads/imagick_win_x86.zip', join(self.build_temp, 'libraries.zip'))
        extract(join(self.build_temp, 'libraries.zip'), lib_base)
        
        return result

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
