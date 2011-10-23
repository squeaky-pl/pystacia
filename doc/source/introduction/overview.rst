Overview
========

The philiosophy
---------------

tinyimg is an object oriented imaging library. It uses factory functions to
create objects representing concepts like :class:`tinyimg.image.Image` or
:class:`tinyimg.image.Color`. You don't typically use class constructors to
create objects and generally you shouldn't unless you really know what you
are doing.

    from tinyimg import read
    image = read('example.jpg')

tinyimg uses symbolic names

tinyimg groups it's functionality into several modules

tinyimg groups all the convenience

Behind the scenes
-----------------