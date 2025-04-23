from __future__ import annotations

import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Protocol, TypedDict, TypeVar

import pytest

from propcache.api import under_cached_property

if sys.version_info >= (3, 11):
    from typing import assert_type

_T_co = TypeVar("_T_co", covariant=True)


class APIProtocol(Protocol):
    def under_cached_property(
        self, func: Callable[[Any], _T_co]
    ) -> under_cached_property[_T_co]: ...


def test_under_cached_property(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            self._cache: dict[str, int] = {}

        @propcache_module.under_cached_property
        def prop(self) -> int:
            return 1

        @propcache_module.under_cached_property
        def prop2(self) -> str:
            return "foo"

    a = A()
    if sys.version_info >= (3, 11):
        assert_type(a.prop, int)
    assert a.prop == 1
    if sys.version_info >= (3, 11):
        assert_type(a.prop2, str)
    assert a.prop2 == "foo"


def test_under_cached_property_typeddict(propcache_module: APIProtocol) -> None:
    """Test static typing passes with TypedDict."""

    class _Cache(TypedDict, total=False):
        prop: int
        prop2: str

    class A:
        def __init__(self) -> None:
            self._cache: _Cache = {}

        @propcache_module.under_cached_property
        def prop(self) -> int:
            return 1

        @propcache_module.under_cached_property
        def prop2(self) -> str:
            return "foo"

    a = A()
    if sys.version_info >= (3, 11):
        assert_type(a.prop, int)
    assert a.prop == 1
    if sys.version_info >= (3, 11):
        assert_type(a.prop2, str)
    assert a.prop2 == "foo"


def test_under_cached_property_assignment(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            self._cache: dict[str, Any] = {}

        @propcache_module.under_cached_property
        def prop(self) -> None:
            """Mock property."""

    a = A()

    with pytest.raises(AttributeError):
        a.prop = 123  # type: ignore[assignment]


def test_under_cached_property_without_cache(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            """Init."""
            self._cache: dict[str, int] = {}

        @propcache_module.under_cached_property
        def prop(self) -> None:
            """Mock property."""

    a = A()

    with pytest.raises(AttributeError):
        a.prop = 123  # type: ignore[assignment]


def test_under_cached_property_check_without_cache(
    propcache_module: APIProtocol,
) -> None:
    class A:
        def __init__(self) -> None:
            """Init."""
            # Note that self._cache is intentionally missing
            # here to verify AttributeError

        @propcache_module.under_cached_property
        def prop(self) -> None:
            """Mock property."""

    a = A()
    with pytest.raises(AttributeError):
        _ = a.prop  # type: ignore[call-overload]


def test_under_cached_property_caching(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            self._cache: dict[str, int] = {}

        @propcache_module.under_cached_property
        def prop(self) -> int:
            """Docstring."""
            return 1

    a = A()
    assert a.prop == 1


def test_under_cached_property_class_docstring(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            """Init."""

        @propcache_module.under_cached_property
        def prop(self) -> None:
            """Docstring."""

    if TYPE_CHECKING:
        # At type checking, the fixture doesn't represent the real module, so
        # we use the global-level imported module to verify the isinstance() check here
        # matches the behaviour users would see in real code.
        assert isinstance(A.prop, under_cached_property)
    else:
        assert isinstance(A.prop, propcache_module.under_cached_property)
    assert "Docstring." == A.prop.__doc__


def test_ensured_wrapped_function_is_accessible(propcache_module: APIProtocol) -> None:
    """Test that the wrapped function can be accessed from python."""

    class A:
        def __init__(self) -> None:
            """Init."""
            self._cache: dict[str, int] = {}

        @propcache_module.under_cached_property
        def prop(self) -> int:
            """Docstring."""
            return 1

    a = A()
    assert A.prop.wrapped(a) == 1
