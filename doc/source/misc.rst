Miscellaneous
=============

.. _search-path:

Skipping binary install
-----------------------

Pystacia to work requires :term:`ImageMagick` shared libraries. Specifically
:term:`MagickWand` DLL. Pystacia by default does install prebuilt binaries.
Sometimes you may want to compile :term:`ImageMagick` yourself and not use packaged
one. You can set environment variable ``PYSTACIA_SKIP_BINARIES`` to non-false
value while performing installation to skip copying of DLLs.

....$ PYSTACIA_SKIP_BINARIES=1 pip install pystacia

Library search path
-------------------

When performing :term:'MagickWand' search theses directories are inspected in
following order:

- ``PYSTACIA_LIBRARY_PATH`` if set 
- `cdll` subdirectory under package install location if ``PYSTACIA_SKIP_PACKAGE``
  is not set
- if inside :term:`virtualenv` subdirectories `lib` and `cdll` under
  ``VIRTUAL_ENV`` are also inspected
- system-wide locations

When loading a library SONAMEs in file names are preferred in this order: 5, 4, 3 and
no SONAME.

Subclassing Image class
-----------------------

Any factory function inside Pystcia can accept optional factory parameter specifying
class or function to be used when instantiating objects.

>>> from pystacia import Image
>>> class MyImage(Image):
>>>     def cool_effect(self):
>>>         self.swirl(45) 
>>> from pystacia import wizard
>>> img = wizard(factory=MyImage)
>>> img
<MyImage(w=480,h=640,8bit,rgb,palette) object at 0x103297200L>
>>> img.cool_effect()

Environment variables influencing pystacia runtime
-------------------------------------------------

- ``PYSTACIA_SKIP_BINARIES`` -- if set no binary :term:`ImageMagick` build is copy in
  `setup.py`
- ``PYSTACIA_LIBRARY_PATH`` -- prepend this path to :term:`MagickWand` search path
- ``PYSTACIA_SKIP_PACKAGE`` -- skip inspecting package `cdll` subdirectory on DLL
  search effectively discarding pre-build binaries even if they are installed
- ``PYSTACIA_SKIP_VIRTUALENV`` -- skip inspecting `lib` and `dll` subdirectories
  if package was installed under :term:`virtualenv`. 
- ``PYSTACIA_NO_CHAINS`` -- disable chaining