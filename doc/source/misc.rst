Miscellaneous
=============

.. _search-path:

Skipping binary install
-----------------------

tinyimg to work requires :term:`ImageMagick` shared libraries. Specifically
:term:`MagickWand` DLL. tinyimg by default does install prebuilt binaries.
Sometimes you may want to compile :term:`ImageMagick` yourself and not use packaged
one. You can set environment variable ``TINYIMG_SKIP_BINARIES`` to non-false
value while performing installation to skip copying of DLLs.

....$ TINYIMG_SKIP_BINARIES=1 pip install tinyimg

Library search path
-------------------

When performing :term:'MagickWand' search theses directories are inspected in
following order:

- ``TINYIMG_LIBRARY_PATH`` if set 
- `cdll` subdirectory under package install location if ``TINYIMG_SKIP_PACKAGE``
  is not set
- if inside :term:`virtualenv` subdirectories `lib` and `cdll` under
  ``VIRTUAL_ENV`` are also inspected
- system-wide locations

When loading a library SONAMEs in file names are preferred in this order: 5, 4, 3 and
no SONAME.

Subclassing tinyimg Image class
-------------------------------

Any factory function inside tinyimg can accept optional factory parameter specifying
class or function to be used when instantiating objects.

>>> from tinyimg import Image
>>> class MyImage(Image):
>>>     def cool_effect(self):
>>>         self.swirl(45) 
>>> from tinyimg import wizard
>>> img = wizard(factory=MyImage)
>>> img
<MyImage(w=480,h=640,8bit,rgb,palette) object at 0x103297200L>
>>> img.cool_effect()

Environment variables influencing tinyimg runtime
-------------------------------------------------

- ``TINYIMG_SKIP_BINARIES`` -- if set no binary :term:`ImageMagick` build is copy in
  `setup.py`
- ``TINYIMG_LIBRARY_PATH`` -- prepend this path to :term:`MagickWand` search path
- ``TINYIMG_SKIP_PACKAGE`` -- skip inspecting package `cdll` subdirectory on DLL
  search effectively discarding pre-build binaries even if they are installed
- ``TINYIMG_SKIP_VIRTUALENV`` -- skip inspecting `lib` and `dll` subdirectories
  if package was installed under :term:`virtualenv`. 
- ``TINYIMG_NO_CHAINS`` -- disable chaining