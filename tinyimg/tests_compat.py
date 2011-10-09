from unittest import TestCase

# we need backported verion of unittest
if not hasattr(TestCase, 'assertSequenceEqual'):
    from unittest2 import TestCase
