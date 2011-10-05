class Enum(object):
    def __init__(self, name):
        self.name = name
        
    def __getattr__(self, name):
        return EnumValue(self, name)
    
    def __repr__(self):
        template = formattable("tinyimg.enum('{0}')")
        
        return template.format(self.name)
        
class EnumValue(object):
    def __init__(self, enum, name):
        self.enum = enum
        self.name = name
        
    def __repr__(self):
        return repr(self.enum) + '.' + self.name

from tinyimg.utils import memoized

@memoized
def enum(name):
    return Enum(name) 

from tinyimg.compat import formattable