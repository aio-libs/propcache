# cython: language_level=3, freethreading_compatible=True

from ._helpers_c cimport cached_property, under_cached_property

# WARNING: Do not use under normal circumstances
# feel free to ignore this file if your not testing.

cdef class TestUnderCachedProperty:
    cdef:
        public dict _cache

    def __init__(self) -> None:
        self._cache = {}

    @under_cached_property
    def prop(self) -> int:
        return 1

    @under_cached_property
    def prop2(self) -> str:
        return "foo"

cdef class TestCachedProperty:
    cdef:
        dict __dict__

    def __init__(self) -> None:
        pass

    @cached_property
    def prop(self) -> int:
        return 1

    @cached_property
    def prop2(self) -> str:
        return "foo"


cdef class TestUnderCachedPropertyAssignment:
    cdef:
        public dict _cache

    def __init__(self) -> None:
        self._cache = {}

    @cached_property
    def prop(self) -> int:
        return 1
