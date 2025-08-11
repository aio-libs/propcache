# cython: language_level=3, freethreading_compatible=True

from propcache cimport cached_property, under_cached_property


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
        public dict _cache
    
    def __init__(self) -> None:
        self._cache = {}

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


