import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

import pytest

from propcache.api import under_cached_property_with_name

if sys.version_info >= (3, 11):
    from typing import assert_type

_T_co = TypeVar("_T_co", covariant=True)


class _CacheNameFactory(Protocol):
    def __call__(
        self, wrapped: Callable[[Any], _T_co]
    ) -> "under_cached_property_with_name[_T_co]": ...


class APIProtocol(Protocol):
    @staticmethod
    def under_cached_property_with_name(
        func: Callable[[Any], _T_co], cache_name: str
    ) -> "under_cached_property_with_name[_T_co]": ...

    @staticmethod
    def under_cache_name(name: str) -> _CacheNameFactory: ...


def test_under_cached_property_with_name(propcache_module: APIProtocol) -> None:
    reify = propcache_module.under_cache_name("_my_cache")

    class A:
        def __init__(self) -> None:
            self._my_cache: dict[str, Any] = {}

        @reify
        def prop(self) -> int:
            return 1

        @reify
        def prop2(self) -> str:
            return "foo"

    a = A()
    if sys.version_info >= (3, 11):
        assert_type(a.prop, int)
        assert_type(a.prop2, str)
    assert a.prop == 1
    assert a.prop2 == "foo"
    assert a._my_cache == {"prop": 1, "prop2": "foo"}


def test_under_cached_property_with_name_assignment(
    propcache_module: APIProtocol,
) -> None:
    reify = propcache_module.under_cache_name("_my_cache")

    class A:
        def __init__(self) -> None:
            self._my_cache: dict[str, Any] = {}

        @reify
        def prop(self) -> None:
            """Mock property."""

    a = A()
    with pytest.raises(AttributeError):
        a.prop = 123  # type: ignore[assignment]


def test_under_cached_property_with_name_missing_cache(
    propcache_module: APIProtocol,
) -> None:
    """Accessing the property before the cache attribute exists must raise."""
    reify = propcache_module.under_cache_name("_my_cache")

    class A:
        @reify
        def prop(self) -> int:
            return 1

    a = A()
    with pytest.raises(AttributeError):
        _ = a.prop


def test_under_cached_property_with_name_caching(
    propcache_module: APIProtocol,
) -> None:
    """The wrapped function must be invoked at most once per instance."""
    calls = 0
    reify = propcache_module.under_cache_name("_my_cache")

    class A:
        def __init__(self) -> None:
            self._my_cache: dict[str, int] = {}

        @reify
        def prop(self) -> int:
            nonlocal calls
            calls += 1
            return 42

    a = A()
    assert a.prop == 42
    assert a.prop == 42
    assert calls == 1


def test_under_cached_property_with_name_isolated_caches(
    propcache_module: APIProtocol,
) -> None:
    """Properties bound to different cache attributes stay independent."""
    in_first = propcache_module.under_cache_name("_first")
    in_second = propcache_module.under_cache_name("_second")

    class A:
        def __init__(self) -> None:
            self._first: dict[str, int] = {}
            self._second: dict[str, int] = {}

        @in_first
        def prop_a(self) -> int:
            return 1

        @in_second
        def prop_b(self) -> int:
            return 2

    a = A()
    assert a.prop_a == 1
    assert a.prop_b == 2
    assert a._first == {"prop_a": 1}
    assert a._second == {"prop_b": 2}


def test_under_cached_property_with_name_descriptor_access(
    propcache_module: APIProtocol,
) -> None:
    """Accessing the descriptor on the class returns the descriptor itself."""
    reify = propcache_module.under_cache_name("_my_cache")

    class A:
        @reify
        def prop(self) -> int:
            """Docstring."""
            return 1

    if TYPE_CHECKING:
        assert isinstance(A.prop, under_cached_property_with_name)
    else:
        assert isinstance(A.prop, propcache_module.under_cached_property_with_name)
    assert A.prop.__doc__ == "Docstring."
    assert A.prop.cache_name == "_my_cache"


def test_under_cached_property_with_name_direct_construction(
    propcache_module: APIProtocol,
) -> None:
    """The descriptor class can be used directly without the factory."""

    def fn(self: "A") -> int:
        return 7

    descriptor = propcache_module.under_cached_property_with_name(fn, "_bucket")

    class A:
        def __init__(self) -> None:
            self._bucket: dict[str, int] = {}

        prop = descriptor

    a = A()
    assert a.prop == 7
    assert a._bucket == {"fn": 7}


def test_under_cache_name_attribute(propcache_module: APIProtocol) -> None:
    """The factory exposes the bound cache name as an attribute."""
    factory = propcache_module.under_cache_name("_my_cache")
    assert factory.cache_name == "_my_cache"  # type: ignore[attr-defined]


def test_under_cached_property_with_name_slots(propcache_module: APIProtocol) -> None:
    """The variant works on classes that use ``__slots__``."""
    reify = propcache_module.under_cache_name("_my_cache")

    class A:
        __slots__ = ("_my_cache",)

        def __init__(self) -> None:
            self._my_cache: dict[str, int] = {}

        @reify
        def prop(self) -> int:
            return 99

    a = A()
    assert a.prop == 99
    assert a._my_cache == {"prop": 99}
