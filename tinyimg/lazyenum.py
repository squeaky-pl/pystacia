class Enum(object):
    def __init__(self, name):
        self.name = name
        
    def __getattr__(self, name):
        return EnumValue(self, name)
        
class EnumValue(object):
    def __init__(self, enum, name):
        self.enum = enum
        self.name = name

from tinyimg.utils import memoized

@memoized
def enum(name):
    return Enum(name) 