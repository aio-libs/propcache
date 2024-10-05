.. propcache documentation master file, created by
   sphinx-quickstart on Mon Aug 29 19:55:36 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

propcache
=========

The module provides accelerated versions of ``cached_property``

Introduction
------------

Usage
-----

The API is designed to be nearly identical to the built-in ``cached_property`` class,
except for the additional ``under_cached_property`` class which uses ``self._cache``
instead of ``self.__dict__`` to store the cached values and prevents ``__set__`` from being called.

API documentation
------------------

Open :ref:`propcache-api` for reading full list of available methods.

Source code
-----------

The project is hosted on GitHub_

Please file an issue on the `bug tracker
<https://github.com/aio-libs/propcache/issues>`_ if you have found a bug
or have some suggestion in order to improve the library.

Discussion list
---------------

*aio-libs* google group: https://groups.google.com/forum/#!forum/aio-libs

Feel free to post your questions and ideas here.


Authors and License
-------------------

The ``propcache`` package is derived from ``yarl`` which is written by Andrew Svetlov.

It's *Apache 2* licensed and freely available.



Contents:

.. toctree::
   :maxdepth: 2

   api

.. toctree::
   :caption: What's new

   changes

.. toctree::
   :caption: Contributing

   contributing/guidelines

.. toctree::
   :caption: Maintenance

   contributing/release_guide


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _GitHub: https://github.com/aio-libs/propcache
