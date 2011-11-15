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
        for subdir in '', 'cdll', 'lib', 'dll', 'depends':
            path = join(tmproot, subdir)
            if not exists(path):
                mkdir(path)
            
            for osname in 'macos', 'linux', 'windows':
                for abi in 2, 1, None:
                    template = formattable(dll_template(osname, abi))
                    libpath = join(path,
                                   template.format(name='Foo', abi=abi)) 
                    open(libpath, 'w').close()
        
        depends = open(join(tmproot, 'depends', 'depends.txt'), 'w')
        depends.write('Depends 18\n')
        depends.close()
        
    def setUp(self):
        self.environ = {'PYSTACIA_SKIP_SYSTEM': '1', 'PYSTACIA_SKIP_PACKAGE': '1'}
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
        # this should find something on supported OS, if it fails you need
        # to add os_name(), dll_template() support and update setUpClass
        self.assertNotEqual(
            find_library('Foo', (2, 1, None), environ, None, MockFactory()),
            None)
        # this should trick dll_template() to return None
        self.assertEqual(
            find_library('Foo', (2, 1, None), environ,
                         '_dummy_os', MockFactory()),
                         None)
    
    def test_order(self):
        environ = self.environ
        environ['PYSTACIA_LIBRARY_PATH'] = self.tmproot
        
        v = find_library('Foo', (2,), environ, 'windows', MockFactory())
        self.assertEqual(basename(v), 'libFoo-2.dll')
        
        v = find_library('Foo', (1, None), environ, 'linux', MockFactory())
        self.assertEqual(basename(v), 'libFoo.so.1')
        
        v = find_library('Foo', (None,), environ, 'macos', MockFactory()) 
        self.assertEqual(basename(v), 'libFoo.dylib')
        
    def test_library_path(self):
        environ = self.environ
        tmproot = environ['PYSTACIA_LIBRARY_PATH'] = self.__class__.tmproot
        
        value = find_library('Foo', (2,), environ, 'windows', MockFactory())
        expect = join(tmproot, 'libFoo-2.dll')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (1, None), environ, 'linux', MockFactory())
        expect = join(tmproot, 'libFoo.so.1')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (None,), environ, 'macos', MockFactory()) 
        expect = join(tmproot, 'libFoo.dylib')
        self.assertEqual(realpath(value), realpath(expect))
        
    def test_venv(self):
        environ = self.environ
        tmproot = environ['VIRTUAL_ENV'] = self.__class__.tmproot
        
        value = find_library('Foo', (2,), environ, 'windows', MockFactory())
        expect = join(tmproot, 'lib', 'libFoo-2.dll')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (1, None), environ, 'linux', MockFactory())
        expect = join(tmproot, 'lib', 'libFoo.so.1')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (None,), environ, 'macos', MockFactory()) 
        expect = join(tmproot, 'lib', 'libFoo.dylib')
        self.assertEqual(realpath(value), realpath(expect))
        
        environ['PYSTACIA_SKIP_VIRTUAL_ENV'] = '1'
        value = find_library('Foo', (None,), environ, 'macos', MockFactory()) 
        self.assertEqual(value, None)
        
    def test_curdir(self):
        environ = self.environ
        tmproot = self.__class__.tmproot
        chdir(tmproot)
        
        value = find_library('Foo', (2,), environ, 'windows', MockFactory())
        expect = join(tmproot, 'libFoo-2.dll')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (1, None), environ, 'linux', MockFactory())
        expect = join(tmproot, 'libFoo.so.1')
        self.assertEqual(realpath(value), realpath(expect))
        
        value = find_library('Foo', (None,), environ, 'macos', MockFactory()) 
        expect = join(tmproot, 'libFoo.dylib')
        self.assertEqual(realpath(value), realpath(expect))
        
    def test_depends(self):
        this_environ = self.environ.copy()
        tmproot = join(self.__class__.tmproot, 'depends')
        this_environ['PYSTACIA_LIBRARY_PATH'] = tmproot
        
        environ = this_environ.copy()
        factory = MockFactory()
        find_library('Foo', (2,), environ, 'windows', factory)
        expect = [join(tmproot, x) for x in ['libDepends-18.dll', 'libFoo-2.dll']]
        self.assertEqual(factory.args, expect)
        
        environ = this_environ.copy()
        factory = MockFactory()
        find_library('Foo', (None,), environ, 'linux', factory)
        expect = [join(tmproot, x) for x in ['libDepends.so.18', 'libFoo.so']]
        self.assertEqual(factory.args, expect)
        
        # throws an exception so shouldnt find anything
        environ = this_environ.copy()
        factory = MockFactory(throw=True)
        value = find_library('Foo', (1,), environ, 'macos', factory)
        expect = [join(tmproot, x) for x in ['libDepends.18.dylib', 'libFoo.1.dylib']]
        self.assertEqual(value, None)
        self.assertEqual(factory.args, expect)
        
        # add DYLD_LIBRARY_PATH to environ for extra coverage
        environ = this_environ.copy()
        factory = MockFactory(throw=True)
        environ['DYLD_FALLBACK_LIBRARY_PATH'] = '/'
        find_library('Foo', (1,), environ, 'macos', factory)
        
    def test_system_wide(self):
        environ = {'PYSTACIA_SKIP_PACKAGE': '1',
                   'PYSTACIA_SKIP_VIRTUAL_ENV': '1',
                   'PYSTACIA_SKIP_CWD': '1'}
        self.assertEqual(find_library('_YourNonExistant', (None,), environ),
                         None)

class GetDllTest(TestCase):
    def test(self):
        environ = {'PYSTACIA_SKIP_PACKAGE': '1',
                   'PYSTACIA_SKIP_VIRTUAL_ENV': '1',
                   'PYSTACIA_SKIP_CWD': '1',
                   'PYSTACIA_SKIP_SYSTEM': '1'}
        
        self.assertRaisesRegexp(PystaciaException, 'Could not find or load',
                                lambda: get_dll(environ=environ))


class GetBridgeTest(TestCase):
    def test(self):
        self.assertIsInstance(get_bridge.undecorated().impl, ThreadImpl)
        bridge = get_bridge.undecorated({'PYSTACIA_IMPL': 'simple'})
        self.assertIsInstance(bridge.impl, SimpleImpl)


class MockFactory(object):
    def __init__(self, throw=False):
        self.args = []
        self.throw = throw
        
    def __call__(self, arg):
        self.args.append(arg)
        
        if self.throw:
            raise PystaciaException('Error')


from tempfile import mkdtemp
from os import getcwd, chdir, mkdir
from os.path import join, basename, exists, realpath
from shutil import rmtree

from pystacia.api import get_dll, dll_template, find_library, get_bridge
from pystacia.bridge import ThreadImpl, SimpleImpl
from pystacia.compat import formattable
from pystacia.util import PystaciaException