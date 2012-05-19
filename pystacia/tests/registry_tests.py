# coding: utf-8
# pystacia/tests/registry_tests.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from time import sleep
from random import sample, randint
from threading import Thread

from pystacia.tests.common import TestCase


class RegistryTest(TestCase):
    def setUp(self):
        self.registry = Registry()
        
    def test_simple(self):
        registry = self.registry
        
        registry.value = 2
        self.assertEquals(registry.value, 2)
        self.assertTrue(hasattr(registry, 'value'))
        self.assertEqual(registry.get('value', 3), 2)
        self.assertEqual(registry.get('value', 3, 3), 3)
        del registry.value
        self.assertFalse(hasattr(registry, 'value'))
        self.assertEqual(registry.get('value', 3), 3)
        self.assertEqual(registry.get('value', 3, 2), 2)
        self.assertRaises(AttributeError, lambda: registry.value)
        
    def test_defaults(self):
        registry = self.registry
        
        registry._install_default('value', 4)
        self.assertEqual(registry.value, 4)
        registry.value = 5
        self.assertEqual(registry.value, 5)
        del registry.value
        self.assertEquals(registry.value, 4)
        
    def test_lock(self):
        registry = self.registry
        
        registry.value = 3
        registry._lock('value')
        self.assertEquals(registry.value, 3)
        
        def assign():
            registry.value = 4
        
        self.assertRaisesRegexp(PystaciaException, 'has been locked',
                                assign)
        
        def delete():
            del registry.value
        
        self.assertRaisesRegexp(PystaciaException, 'has been locked',
                                delete)
    
    def test_threaded(self):
        registry = self.registry
        
        for x in range(0, 20):
            setattr(registry, 'value_' + str(x), x)
        
        def thread():
            sleep(0.01)
            for x in sample(range(0, 20), 18):
                self.assertEqual(getattr(registry, 'value_' + str(x)), x)
                if randint(0, 1):
                    registry._install_default('value_' + str(x), 2 * x)
        
        threads = [Thread(target=thread) for _ in range(0, 50)]
        [t.start() for t in threads[:10]]
        
        for x in range(0, 15):
            registry._lock('value_' + str(x))
        
        [t.start() for t in threads[10:]]
        
        for x in range(15, 20):
            registry._lock('value_' + str(x))
        
        [t.join() for t in threads]

from pystacia.registry import Registry
from pystacia.util import PystaciaException
