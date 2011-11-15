# coding: utf-8
# pystacia/api/tests/__init__.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


from pystacia.tests.common import TestCase



class TemplateTest(TestCase):
    def test(self):
        self.assertEqual(dll_template('macos', 1), 'lib{name}.{abi}.dylib')
        self.assertEqual(dll_template('macos', None), 'lib{name}.dylib')
        self.assertEqual(dll_template('linux', 2), 'lib{name}.so.{abi}')
        self.assertEqual(dll_template('linux', None), 'lib{name}.so')
        self.assertEqual(dll_template('windows', 3), 'lib{name}-{abi}.dll')
        self.assertEqual(dll_template('windows', None), 'lib{name}.dll')
        self.assertEqual(dll_template('_dummy', None), None)


class FindLibraryTest(TestCase):
    @classmethod
    def setUpClass(cls):
        tmproot = cls.tmproot = mkdtemp()
        for subdir in '', 'cdll', 'lib', 'dll':
            path = join(tmproot, subdir)
            if not exists(path):
                mkdir(path)
            
            for osname in 'macos', 'linux', 'windows':
                for abi in 2, 1, None:
                    template = formattable(dll_template(osname, abi))
                    libpath = join(path,
                                   template.format(name='Foo', abi=abi)) 
                    open(libpath, 'w').close()
        
    def setUp(self):
        self.environ = {'PYSTACIA_FAKE': '1', 'PYSTACIA_SKIP_PACKAGE': '1'}
        self.olddir = getcwd()
        
    def tearDown(self):
        chdir(self.olddir)
        
    @classmethod
    def tearDownClass(cls):
        rmtree(cls.tmproot)
    
    def test(self):
        environ = self.environ
        environ['PYSTACIA_LIBRARY_PATH'] = self.tmproot
        
        self.assertEqual(find_library('Bar', (2, 1, None)), None)
        self.assertEqual(find_library('Foo', ()), None)
        self.assertEqual(find_library('Foo', (2, 1, None), {}), None)
        self.assertNotEqual(find_library('Foo', (2, 1, None), environ, None),
                            None)
    
    def test_order(self):
        environ = self.environ
        environ['PYSTACIA_LIBRARY_PATH'] = self.tmproot
        
        v = find_library('Foo', (2,), environ, 'windows')
        self.assertEqual(basename(v), 'libFoo-2.dll')
        
        v = find_library('Foo', (1, None), environ, 'linux')
        self.assertEqual(basename(v), 'libFoo.so.1')
        
        v = find_library('Foo', (None,), environ, 'macos') 
        self.assertEqual(basename(v), 'libFoo.dylib')
        
    def test_library_path(self):
        environ = self.environ
        tmproot = environ['PYSTACIA_LIBRARY_PATH'] = self.__class__.tmproot
        
        value = find_library('Foo', (2,), environ, 'windows')
        expect = join(tmproot, 'libFoo-2.dll')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (1, None), environ, 'linux')
        expect = join(tmproot, 'libFoo.so.1')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (None,), environ, 'macos') 
        expect = join(tmproot, 'libFoo.dylib')
        self.assertEqual(realpath(value), realpath(expect))
        
    def test_venv(self):
        environ = self.environ
        tmproot = environ['VIRTUAL_ENV'] = self.__class__.tmproot
        
        value = find_library('Foo', (2,), environ, 'windows')
        expect = join(tmproot, 'lib', 'libFoo-2.dll')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (1, None), environ, 'linux')
        expect = join(tmproot, 'lib', 'libFoo.so.1')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (None,), environ, 'macos') 
        expect = join(tmproot, 'lib', 'libFoo.dylib')
        self.assertEqual(realpath(value), realpath(expect))
        
        environ['PYSTACIA_SKIP_VIRTUAL_ENV'] = '1'
        value = find_library('Foo', (None,), environ, 'macos') 
        self.assertEqual(value, None)
        
    def test_curdir(self):
        environ = self.environ
        tmproot = self.__class__.tmproot
        chdir(tmproot)
        
        value = find_library('Foo', (2,), environ, 'windows')
        expect = join(tmproot, 'libFoo-2.dll')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (1, None), environ, 'linux')
        expect = join(tmproot, 'libFoo.so.1')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (None,), environ, 'macos') 
        expect = join(tmproot, 'libFoo.dylib')
        self.assertEqual(realpath(value), realpath(expect))

from tempfile import mkdtemp
from os import getcwd, chdir, mkdir
from os.path import join, basename, exists, realpath
from shutil import rmtree

from pystacia.api import dll_template, find_library
from pystacia.compat import formattable