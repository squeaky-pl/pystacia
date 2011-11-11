def get_options():
    options = {}
    
    size = c_size_t()
    keys = c_call('magick_', 'query_configure_options', '*', size)
    for key in (native_str(keys[i]) for i in range(size.value)):
        options[key] = (
        c_call('magick_', 'query_configure_option', key))
        
    return options
    
from ctypes import c_size_t
from pystacia.api.func import c_call
from pystacia.compat import native_str