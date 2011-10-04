from bz2 import BZ2File

# patch BZ2File to support with statement in python <=2.6
if not hasattr(BZ2File, '__exit__'):
    class BZ2Replacement(BZ2File):
        __enter__ = lambda self: self
        __exit__ = lambda self, type, value, traceback: self.close()
        
    BZ2File = BZ2Replacement