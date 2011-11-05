"""Resource management utilities."""


class Resource(object):
    
    """Base class for :term:`ImageMagick` resources.
       
       Serves a base for classes that need to call
       C functions to allocate underlying structures.
       Also keeps track of all objects with weak references
       so they can be freed all at once if they are still
       alive at the time program exits.
       
       Subclasses need to implement three methods: _alloc, _free and _copy to
       conform to the interface.
    """
    
    def __init__(self, resource=None):
        """Construct new instance of resource."""
        self.__resource = resource if resource != None else self._alloc()
        
        if self.__resource == None:
            tmpl = formattable('{0} _alloc method returned None')
            raise PystaciaException(tmpl.format(self.__class__.__name__))
        
        if not id(self) in _registry:
            _registry[id(self)] = self
    
    def _claim(self):
        """Claim resource and close this instance.
           
           This is used to transfer management of underlying
           resource to another
           entity. This instance is closed afterwards.
           
           Not to be called directly under normal circumstances
        """
        resource = self.resource
        self.__resource = None
        
        if not _cleaningup and id(self) in _registry:
            del _registry[id(self)]
        
        return resource
    
    def close(self):
        """Free resource and close the object
           
           Call this method when the object is no longer needed or to free
           the data immediately. It's also automatically called when you
           use with context protocol.
        """
        self._free()
        self._claim()
    
    def copy(self):
        """Get independent copy of this resource."""
        resource = self._clone()
        
        if resource == None:
            tmpl = formattable('{0} _clone method returned None')
            raise PystaciaException(tmpl.format(self.__class__.__name__))
        
        return self.__class__(resource)
    
    @property
    def closed(self):
        """Check if instance is already closed.
           
           Returns ``True`` if object is no longer usable i.e.
           :meth:``pystacia.common.Resource.close`` has been called.
        """
        return self.__resource == None
    
    @property
    def resource(self):
        """Get underlying C resource.
           
           You can use this method to get access to raw C struct that you
           can use with :term:`ctypes` calls directly. It can be useful
           when you want to perform custom operations.
        """
        if self.__resource == None:
            tmpl = formattable('{0} already closed.')
            raise PystaciaException(tmpl.format(self.__class__.__name__))
        
        return self.__resource
    
    def __del__(self):
        """Automatically free object on GC."""
        if not self.closed:
            self.close()


from weakref import WeakValueDictionary

from pystacia.util import PystaciaException
from pystacia.compat import formattable


_registry = WeakValueDictionary()
"""Dictionary keeping references to all resources."""

_cleaningup = False


def _cleanup():
    """Free all tracked intances.
       
       Closes and destroys all currently allocated resources. This gets called
       from atexit handler just before :term:`ImageMagick` gets uninitialized.
    """
    global _cleaningup
    _cleaningup = True
    
    for ref in _registry.itervaluerefs():
        obj = ref()
        if obj:
            if not obj.closed:
                obj.close()
            del obj
