===============================================
The «tinyimg» raster image manipulation library
===============================================

Tinyimg is a down-to-earth image manipulation library born out of practical
needs. It's simple, it's cross-platform, runs on Python 2.5+, 3.x,
:term:`PyPy` and :term:`IronPython`. It's compact but still appropriate for most of your
day to day image handling tasks. Tinyimg leverages powerful :term:`ImageMagick`
library as a back-end exposing easily comprehensible Pythonic API.

Here is one of the simplest code snippets showing what you can do with it:

.. literalinclude:: simple.py

When saved to ``simple.py``, the above script can be run via:

.. code-block:: sh

    $ pip install tinyimg
    $ python simple.py

Provided you have file example.png in the same directory it would output
version of the file which would be scaled to 320╳240 pixels and rotated by 30
degrees. It would also display it in your default system image viewing
program.

Front matter
============

.. toctree::
   :maxdepth: 1
   
   copyright

Narrative documentation
=======================

.. toctree::
   :maxdepth: 3
   
   introduction
   installation
   image
   color
   misc


Reference Material
==================

Reference material includes documentation for tinyimg API.

.. toctree::
   :maxdepth: 2

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

