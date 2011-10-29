Motivation
============


Why another Python imaging library
----------------------------------

There exist quite a bunch of other Python imaging solutions with :term:`PIL`
being the most prominent one. Most of them don't satisfy at least one and
typically more of the criteria that I consider quality and modern
Python software.

- They are hardly documented or not at all
- They don't have complete test suite with reasonable coverage
- They don't work with one of: Python 2.5, Python 2.6, Python 2.7, Python 3.2,
  :term:`PyPy` or :term:`IronPython`
- They can't run processing algorithms on many cores in parallel leaving
  them idle.
- They are limited to narrow scope of image formats
- They don't allow operation on :term:`RAW` data formats such as :term:`YCbCr`
  or :term:`RGB` triplets
- They can only process images internally in 8bit depth per channel what
  can be not sufficient for some operations
- They are not actively maintained anymore or largely out-dated
- They don't provide Pythonic API because they are modeled after :term:`C` code
- They provide interfaces that are not easily extensible e.g. don't allow
  subclassing
- They are not easily installed on widely used OSes such as :term:`Windows`,
  :term:`Linux` and `MacOS X`
- They always require :term:`C` compiler during installation phase
- They don't have transparent open-source development cycle
- They try to hide complexity of image processing preventing you from performing
  custom advance operations
- You can find a lot of ranting on the Internet and they drive you crazy


Why another :term:`ImageMagick` wrapper
---------------------------------------

While you can find a lot of :term:`ImageMagick` wrappers most of them feel
like doing :term:`C++` in Python. Some of them are not maintained and typically
don't work on one of supported Python runtime + platform combinations.

What Pystacia does about that
------------------------------

- Pystacia has documentation that I try to make as complete as my resources let
  me
- Pystacia has large test suite consisting of ~70 tests with 90% coverage at
  the time of writing.
- Pystacia works both on Python 2.5+ and Python 3.x as well as :term:`PyPy`
  and :term:`IronPython`. :term:`Jython` support is planned through
  :term:`JNA` interface or :term:`ctypes` if it gets reasonably stable and
  complete by the time of implementation.
- Pystacia ships version of `ImageMagick` built with :term:`OMP` support
  which lets you use all your cores for image processing.
- Pystacia comes with wide spectrum of supported formats in standard
  distribution. `JPEG`, `PNG`, `TIFF`, `GIF`, `BMP`, `ICO`, `JNG`, `PCX`, `PNM`,
  `HDR`, `EXR` to name a few. See http://www.imagemagick.org/script/formats.php
  for complete list.
- Pystacia can read and write :term:`RAW` data blobs such as `RGB`, `YCbCr`,
  `YUV` and `CMYK` in both 8 and 16 bits per channel
  with or without alpha channel directly from Python strings or streams.
- The default :term:`ImageMagick` distribution coming with Pystacia processes
  data in 16 bit precision internally.
- I did put a lot of effort into making this code as good as possible.
  All the Python code is continously tested against PEP8 validity and inspected
  with :term:`Pyflakes` to detect common problems.
- Pystacia tries to hide :term:`ImageMagick` quirks, shield you from ABI changes,
  provide monolithic Python API. It supports any version of Imagick that is
  newer or equal to 6.5.9.0. Pystacia itself comes with reasonable recent
  versions of :term:`ImageMagick`.
- Pystacia strives to provide Pythonic API employing as many idioms and common
  patterns as possible. Pystacia classes are fully subclassable and factory
  methods can accept factory parameters which specify which class is to be used.
- Pystacia comes with prebuild :term:`ImageMagick` binaries for Windows, Linux and
  MacOS X. Still it's possible to build it yourself if the default distribution
  doesn't fit your needs.
- Pystacia is completely free of charge both for open-source and commercial uses
  as it's licensed under
  `MIT license <http://www.opensource.org/licenses/mit-license.php>`_.
- Pystacia exposes wand property on objects so you can use raw `ctypes` calls
  if you really want to but normally it shouldn't be necessary.