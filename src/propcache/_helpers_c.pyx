# cython: language_level=3, freethreading_compatible=True
from types import GenericAlias

# Added to prevent performance from degrading in the most critical sections.
cdef extern from "Python.h":
    """
/* Fixes performance regression when generating cython code. */
/* SEE: https://github.com/aio-libs/propcache/issues/244 */
static PyObject*
under_cached_property_get(
    PyObject* wrapped,
    PyObject* name,
    PyObject* cache,
    PyObject* inst
)
{
    PyObject* val;

    if (!PyDict_Check(cache)){
        PyErr_Format(
            PyExc_TypeError,
            "Expected dict, got %.200s",
            Py_TYPE(cache)->tp_name
        );
        return NULL;
    }


    val = PyDict_GetItem(cache, name);
    if (val == NULL){
        val = PyObject_CallOneArg(wrapped, inst);
        if (val == NULL){
            return NULL;
        }
        if (PyDict_SetItem(cache, name, val) < 0){
            Py_CLEAR(val);
            return NULL;
        }
        return val;  /* already owned the ref from CallOneArg */
    }
    Py_INCREF(val);  /* borrowed from PyDict_GetItem */
    return val;
}
    """
    object under_cached_property_get(
        object wrapped,
        object name,
        object cache,
        object inst
    )


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
        return under_cached_property_get(self.wrapped, self.name, inst._cache, inst)

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
        return under_cached_property_get(self.func, self.name, inst.__dict__, inst)

    __class_getitem__ = classmethod(GenericAlias)
