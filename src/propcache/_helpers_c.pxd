cdef class under_cached_property:
    # Use as a class method decorator.  It operates almost exactly like
    # the Python `@property` decorator, but it puts the result of the
    # method it decorates into the instance dict after the first call,
    # effectively replacing the function it decorates with an instance
    # variable.  It is, in Python parlance, a data descriptor.

    cdef readonly object wrapped
    cdef object name

cdef class cached_property:
    # Use as a class method decorator.  It operates almost exactly like
    # the Python `@property` decorator, but it puts the result of the
    # method it decorates into the instance dict after the first call,
    # effectively replacing the function it decorates with an instance
    # variable.  It is, in Python parlance, a data descriptor.

    cdef readonly object func
    cdef object name
