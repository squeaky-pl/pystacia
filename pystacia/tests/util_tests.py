# coding: utf-8
# pystacia/tests/util_tests.py
# Copyright (C) 2011 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import math
from random import randint, choice

from pystacia.tests.common import TestCase, skipIf


class MemoizedTest(TestCase):
    def test(self):
        a = producer()
        
        self.assertEqual(producer(), a)
        self.assertEqual(add(1, 2), 3)
        self.assertNotEqual(producer(1), a)
        
    def test_threaded(self):
        def thread():
            for _ in range(randint(0, 20)):
                a = randint(0, 100)
                b = randint(0, 100)
                self.assertEqual(add(a, b), a + b)
        
        threads = [Thread(target=thread) for _ in range(randint(0, 50))]
        [t.start() for t in threads]
        [t.join() for t in threads]
        
    def test_nested(self):
        funcs = [add3, add3, add]
        
        def thread():
            for _ in range(randint(0, 20)):
                func = choice(funcs)
                a = randint(0, 100)
                b = randint(0, 100)
                if func == add:
                    self.assertEqual(func(a, b), a + b)
                elif func == add3:
                    c = randint(0, 100)
                    self.assertEqual(func(a, b, c), a + b + c)
        
        threads = [Thread(target=thread) for _ in range(randint(0, 50))]
        [t.start() for t in threads]
        [t.join() for t in threads]
        
    def test_recursive(self):
        def thread():
            for _ in range(randint(0, 20)):
                a = randint(0, 100)
                self.assertEqual(recurse(a), a)
        
        threads = [Thread(target=thread) for _ in range(randint(0, 50))]
        [t.start() for t in threads]
        [t.join() for t in threads]
    
    @skipIf(not hasattr(math, 'factorial'), 'Python without factorial')
    def test_threaded_recursive(self):
        def thread():
            x = randint(1, 7)
            self.assertEqual(threaded_factorial(x), math.factorial(x))
            
        threads = [Thread(target=thread) for _ in range(0, 50)]
        [t.start() for t in threads]
        [t.join() for t in threads]


class A(object):
    pass

from pystacia.util import memoized


@memoized
def producer(arg=None):
    """doc"""
    return A()


@memoized
def add(a, b):
    return a + b


@memoized
def add3(a, b, c):
    return add(a, b) + c


@memoized
def recurse(i):
    if not i:
        return 0
    else:
        return recurse(i - 1) + 1

from threading import Thread


class SubThread(Thread):
    def __init__(self, i):
        self.i = i
        
        super(SubThread, self).__init__()
        
    def run(self):
        self.result = threaded_factorial(self.i)
            

@memoized
def threaded_factorial(i):
    if i == 1:
        return 1
    else:
        subthread = SubThread(i - 1)
        subthread.start()
        subthread.join()
        
        return i * subthread.result
