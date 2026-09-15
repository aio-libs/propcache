# cython: language_level=3, freethreading_compatible=True
from types import GenericAlias

from cpython.object cimport PyObject


cdef extern from *:
    # ``propcache_get_ref`` looks ``name`` up in ``cache`` and stores a
    # strong reference to the cached value in ``*value``. It returns 1 on a
    # hit, 0 on a miss and -1 with an exception set on error, the same
    # contract as ``PyDict_GetItemRef``. ``propcache_steal`` hands the
    # reference to Cython as an ``object`` without another incref, so a
    # cache hit costs exactly one incref.
    #
    # On the free-threaded build a borrowed pointer from ``PyDict_GetItem``
    # could be freed by a concurrent eviction before it is used, so the
    # atomic ``PyDict_GetItemRef`` is used there instead. On the default
    # build ``PyDict_GetItem`` never reports an error, so the compiler drops
    # the ``except -1`` check entirely.
    """
    static CYTHON_INLINE int
    propcache_get_ref(PyObject *cache, PyObject *name, PyObject **value)
    {
    #ifdef Py_GIL_DISABLED
        return PyDict_GetItemRef(cache, name, value);
    #else
        *value = PyDict_GetItem(cache, name);
        Py_XINCREF(*value);
        return *value != NULL;
    #endif
    }

    #define propcache_steal(value) (value)

    /* Store the new reference ``value`` in ``cache`` and hand it back to
       the caller, or drop it and return NULL if the store fails. */
    static CYTHON_INLINE PyObject *
    propcache_store(PyObject *cache, PyObject *name, PyObject *value)
    {
        if (PyDict_SetItem(cache, name, value) < 0) {
            Py_DECREF(value);
            return NULL;
        }
        return value;
    }
    """
    int propcache_get_ref(object cache, object name, PyObject** value) except -1
    object propcache_steal(PyObject* value)
    object propcache_store(object cache, object name, PyObject* value)


cdef extern from "Python.h":
    # Call a callable Python object callable with exactly
    # 1 positional argument arg and no keyword arguments.
    # Return the result of the call on success, or raise
    # an exception and return NULL on failure.
    PyObject* PyObject_CallOneArg(
        object callable, object arg
    ) except NULL


cdef class under_cached_property:
    """Use as a class method decorator.  It operates almost exactly like
    the Python `@property` decorator, but it puts the result of the
    method it decorates into the instance dict after the first call,
    effectively replacing the function it decorates with an instance
    variable.  It is, in Python parlance, a data descriptor.

    """

    cdef readonly object wrapped
    cdef object name

    def __init__(self, object wrapped):
        self.wrapped = wrapped
        self.name = wrapped.__name__

    @property
    def __doc__(self):
        return self.wrapped.__doc__

    def __get__(self, object inst, owner):
        if inst is None:
            return self
        cdef dict cache = inst._cache
        cdef PyObject* val
        if propcache_get_ref(cache, self.name, &val):
            return propcache_steal(val)
        return propcache_store(
            cache, self.name, PyObject_CallOneArg(self.wrapped, inst)
        )

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

    def __set_name__(self, owner, object name):
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
        cdef PyObject* val
        if propcache_get_ref(cache, self.name, &val):
            return propcache_steal(val)
        return propcache_store(
            cache, self.name, PyObject_CallOneArg(self.func, inst)
        )

    __class_getitem__ = classmethod(GenericAlias)
