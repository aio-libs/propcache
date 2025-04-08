.. _propcache-api:

=========
Reference
=========

.. module:: propcache.api



cached_property
===============

.. decorator:: cached_property(func)

   This decorator functions exactly the same as the standard library
   :func:`cached_property` decorator, but it's available in the
   :mod:`propcache.api` module along with an accelerated Cython version.

   As with the standard library version, the cached value is stored in
   the instance's ``__dict__`` dictionary. To clear a cached value, you
   can use the ``del`` operator on the instance's attribute or call
   ``instance.__dict__.pop('attribute_name', None)``.

under_cached_property
=====================

.. decorator:: under_cached_property(func)

   Transform a method of a class into a property whose value is computed
   only once and then cached as a private attribute. Similar to the
   :func:`cached_property` decorator, but the cached value is stored
   in the instance's ``_cache`` dictionary instead of ``__dict__``.

   Example::

       from propcache.api import under_cached_property

       class MyClass:

           def __init__(self, data: List[float]):
               self._data = data
               self._cache = {}

           @under_cached_property
           def calculated_data(self):
               return expensive_operation(self._data)

           def clear_cache(self):
               self._cache.clear()

       instance = MyClass([1.0, 2.0, 3.0])
       print(instance.calculated_data)  # expensive operation

       instance.clear_cache()
       print(instance.calculated_data)  # expensive operation
