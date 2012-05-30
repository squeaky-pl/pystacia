from distutils.sysconfig import get_python_lib
from os import symlink
from os.path import join

symlink(join(get_python_lib(), 'pystacia/cdll'), 'pystacia/cdll')

