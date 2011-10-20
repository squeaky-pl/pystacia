# coding: utf-8

from distutils.command.build import build

class tinyimg_build(build):
    def run(self):
        result = build.run(self)
        
        from os.path import join 
        from distutils.file_util import write_file
        from distutils.dir_util import mkpath
        
        print('==> Installing binary ImageMagick distribution')
        
        #from pdb import set_trace; set_trace()
        
        lib_base = join(self.build_base, 'libraries')
        mkpath(lib_base)
        write_file(join(lib_base, 'test.txt'), 'test')
        
        return result

from setuptools.command.install import install

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