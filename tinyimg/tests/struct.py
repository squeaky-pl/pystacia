from unittest import TestCase

from ..struct import group

class GroupTestCase(TestCase):
    def test(self):
        self.assertListEqual(group(('a',), 0), [('a', 0)])
        self.assertListEqual(group((), 0), [])
        self.assertListEqual(group(('a', 'b', 'c'), 1), [('a', 1), ('b', 1), ('c', 1)])