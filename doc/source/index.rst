================================================
The «Pystacia» raster image manipulation library
================================================

Pystacia is a new image manipulation library written to meet practical
needs of developers. It's simple, it's cross-platform, runs on Python 2.5+, 3.x,
:term:`PyPy` and :term:`IronPython`. It's compact but still appropriate for most of your
day to day image handling tasks. Pystacia leverages powerful :term:`ImageMagick`
library as a back-end exposing easily comprehensible pythonic :term:`API`.

Here is one of the simplest code snippets showing what you can do with it:

.. literalinclude:: simple.py

When saved to ``simple.py``, the above script can be run via:

.. code-block:: sh

    $ pip install pystacia
    $ python simple.py

Provided you have file ``example.png`` in the same directory it would output
version of the file which would be scaled to 320╳240 pixels and rotated by 30
degrees. It would also display it in your default system image viewing
program.

What's new
==========

.. toctree::
    :maxdepth: 1

    whatsnew/0.2

Front matter
============

.. toctree::
   :maxdepth: 1

   copyright

Narrative documentation
=======================

.. toctree::
   :maxdepth: 2

   introduction
   installation
   image
   color
   misc


Reference Material
==================

Reference material includes documentation for Pystacia :term:`API`.

.. toctree::
   :maxdepth: 2

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
