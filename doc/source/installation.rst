============
Installation
============

Before you install
==================

You will need Python version 2.5 or better or Python 3.x to use tinyimg.

If you don't know how to install Python on your machine please refer to
appropriate section in
`Pyramid documentation <http://docs.pylonsproject.org/projects/pyramid/current/narr/install.html#if-you-don-t-yet-have-a-python-interpreter-unix>`_
where it has been elaborated.

Tinyimg is also known to work with :term:`PyPy` and :term:`IronPython` 2.7.1.
Instructions for running on :term:`PyPy` don't differ from those for
:term:`cPython`. :term:`IronPython` doesn't support :term:`setuptools` yet
so installation must be performed manually by downloading and unpacking
several packages. Refer to :ref:`ironpython` for more details.

Installing tinyimg with cPython or PyPy on Windows, Linux and MacOS
===================================================================

Before proceeding on Windows ensure that Python binary is on your system
search path. When you type `python` in console you should be greeted with
python interactive console.

It is best practice to install develop your applicaion in a “virtual”
Python environment in order to obtain isolation from any “system”
packages you’ve got installed in your Python version. This can be done by
using the :term:`virtualenv` package. Using a virtualenv will also prevent
tinyimg from globally installing versions
of packages that are not compatible with your system Python.

Let's assume that you have following folder structure::

    /workspace
         /my-project
              helloworld.py

Workspace folder is typically a common ancestor folder where you put your Python
projects. My project folder contains all the files related to your poject.

To set up virtualenv you need to grab its latest version from 
https://github.com/pypa/virtualenv/tags. At the time of writing version
1.6.4 was the most up to date one. Download it to Workspace folder, unpack,
delete original ZIP file and rename unpacked folder to virtualenv.

We're going to create your virtual environment which contains all the packages
that your project needs to install in a way that they are separated from
system-wide packages. Open console program, `cd` into Workspace directory and
type following command:

.. code-block:: bash

    $ python virtualenv/virtualenv.py --no-site-packages my-project/my-project-env
    
.. note::

    On Windows change forward slashes to backslashes. If you use :term:`PyPy`
    instead of :term:`cPython` substitute `python` for `pypy` binary name.

This will create my-project/my-project-env with virtual environment in it. You
can put your virtual environment whereever you want but typically you do it
under a subfolder inside your project folder to keep things together.

Now the virtualenv is created you need to activate it so all the feature
commands and installations will be performed in a virtualenv instead of being
applied system-wide. To do so on Linux and Mac perform following command:

.. code-block:: bash

    $ cd my-project
    $ source my-project-env/bin/activate
    
and on Windows:

.. code-block:: bash

    $ cd my-project
    $ my-project-env/Scripts/activate.bat
    
After completing your shell prompt should include my-project-env environment
name in it. You can now install tinyimg inside your virtual environment with
:term:`pip`.

.. code-block:: bash

    $ pip install tinyimg

You can test your installation by performing following action:

.. code-block:: bash

    $ python
    Python 2.7.1 (dcae7aed462b, Aug 17 2011, 09:46:15)
    [PyPy 1.6.0 with GCC 4.0.1] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from tinyimg import lena
    >>> lena().show()
    
It should display nice standard test image depicting
`Lena Söderberg <http://en.wikipedia.org/wiki/Lenna>`_, the first Lady of the
Internet.

.. _ironpython:

Installing tinying with IronPython on Windows and .NET
======================================================

Installing tinyimg on IronPython is manual since at the time of writing
IronPython couldn't handle :term:`virtualenv`, :term:`pip` or :term: `setuptools`
properly. Though it's completely functional with a little bit of effort.

First obtain latest version of IronPython from http://ironpython.net/. At the
time of writing it was 2.7.1. Perform standard installation procedure.

Create your sandbox folder where you install all the needed packages and
perform testing. Let's say it's C:\sandbox.

    C:\sandbox

We need to manually satisfy all the dependencies. First grab :term:six library
from http://pypi.python.org/pypi/six. Download, unpack and copy `six.py` file into
your sandbox folder. Then go to http://pypi.python.org/pypi/decorator grab source
distribution unpack it and grab file `decorator.py` from src subfolder directly
into your sandbox folder. Now your sandbox folder should look like this:

    C:\sandbox
        decorator.py
        six.py

Now it's time to install tinyimg itself. Go to [TODO: link] and grab tinyimg
source distribution, unpack it and put folder tinyimg under your sandbox folder.
You also need a binary image distribution for your Windows. If you use 32 bit
Windows grab it from [TODO: link] or from [TODO: link] if you are on 64 bit
version. Unpack it and move all the files into `cdll` subdirectory under `tinyimg`
folder. Your installation should look like this now::

    C:\sandbox
        decorator.py
        six.py
        tinyimg\
            *some files here*
            cdll\
                *ImageMagick dlls here*

You are almost done. Open your console program and type::

    cd c:\sandbox
    ipy.exe -X:Frames
    >>> from tinyimg import *

If it succeeds everything is configured propertly. Note that we assmued that
`ipy.exe` is on your system path - otherwise you need to type full path to it
Also -X:Frames switch is mandatory since :term:`IronPython` otherwise doesn't
provide :func:`sys._getframe` which is referenced by :term:`decorator` and
:term:`six` libraries. 

What gets installed
===================

Tinyimg relies on :term:`six` library to ship one source code both for Python 2.x
and Python 3.x. It also heavily uses :term:`decorator` library to make decorators
easily documented and accessible with help in Python console. For testing
on Python 2.6 and lower it pulls in :term:`unittest2` library which is
a backport of Python 3.x testing library. On Python 2.5 it
also need :term:`StringFormat` library as a polyfill for missing :meth:`str.format`
method.

I want to run a test suite
==========================

Test suite can be run by entering the tinyimg folder inside site-packages folder
and running `nosetests` after install :term:`nose` package.