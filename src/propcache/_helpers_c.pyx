# cython: language_level=3, freethreading_compatible=True
from types import GenericAlias


cdef _sentinel = object()


cdef class CacheBase:
    """Base class for objects that use cached properties.  This class
    provides a _cache attribute that is used to store the results of
    cached properties.

    Callers are responsible for calling super().__init__() in their
    __init__() methods to ensure that the _cache attribute is
    initialized.
    """

    cdef public dict _cache

    def __init__(self):
        self._cache = {}


cdef class base_cached_property:
    """Use as a class method decorator.  It operates almost exactly like
    the Python `@property` decorator, but it puts the result of the
    method it decorates into the instance dict after the first call,
    effectively replacing the function it decorates with an instance
    variable.  It is, in Python parlance, a data descriptor. This version
    requires that the base class CacheBase is used, which provides
    the _cache attribute.

    """

    cdef readonly object wrapped
    cdef object name

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.name = wrapped.__name__

    @property
    def __doc__(self):
        return self.wrapped.__doc__

    def __get__(self, inst, owner):
        if inst is None:
            return self
        val = (<CacheBase>inst)._cache.get(self.name, _sentinel)
        if val is _sentinel:
            val = self.wrapped(inst)
            (<CacheBase>inst)._cache[self.name] = val
        return val

    def __set__(self, inst, value):
        raise AttributeError("cached property is read-only")

    __class_getitem__ = classmethod(GenericAlias)


cdef class under_cached_property:
    """Use as a class method decorator.  It operates almost exactly like
    the Python `@property` decorator, but it puts the result of the
    method it decorates into the instance dict after the first call,
    effectively replacing the function it decorates with an instance
    variable.  It is, in Python parlance, a data descriptor.

    """

    cdef readonly object wrapped
    cdef object name

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.name = wrapped.__name__

    @property
    def __doc__(self):
        return self.wrapped.__doc__

    def __get__(self, inst, owner):
        if inst is None:
            return self
        cdef dict cache = inst._cache
        val = cache.get(self.name, _sentinel)
        if val is _sentinel:
            val = self.wrapped(inst)
            cache[self.name] = val
        return val

    def __set__(self, inst, value):
        raise AttributeError("cached property is read-only")

    __class_getitem__ = classmethod(GenericAlias)


cdef class cached_property:
    """Use as a class method decorator.  It operates almost exactly like
    the Python `@property` decorator, but it puts the result of the
    method it decorates into the instance dict after the first call,
    effectively replacing the function it decorates with an instance
    variable.  It is, in Python parlance, a data descriptor.

    """

    cdef readonly object func
    cdef object name

    def __init__(self, func):
        self.func = func
        self.name = None

    @property
    def __doc__(self):
        return self.func.__doc__

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
        elif name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                f"({self.name!r} and {name!r})."
            )

    def __get__(self, inst, owner):
        if inst is None:
            return self
        if self.name is None:
            raise TypeError(
                "Cannot use cached_property instance"
                " without calling __set_name__ on it.")
        cdef dict cache = inst.__dict__
        val = cache.get(self.name, _sentinel)
        if val is _sentinel:
            val = self.func(inst)
            cache[self.name] = val
        return val

    __class_getitem__ = classmethod(GenericAlias)
