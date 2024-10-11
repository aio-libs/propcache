from typing import Any, Protocol

import pytest

from propcache.api import under_cached_property


class APIProtocol(Protocol):

    under_cached_property: type[under_cached_property]


def test_under_cached_property(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            self._cache: dict[str, int] = {}

        @propcache_module.under_cached_property
        def prop(self) -> int:
            return 1

    a = A()
    assert a.prop == 1


def test_under_cached_property_class(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            """Init."""

        @propcache_module.under_cached_property
        def prop(self) -> None:
            """Docstring."""

    assert isinstance(A.prop, propcache_module.under_cached_property)
    assert A.prop.__doc__ == "Docstring."


def test_under_cached_property_assignment(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            self._cache: dict[str, Any] = {}

        @propcache_module.under_cached_property
        def prop(self) -> None:
            """Mock property."""

    a = A()

    with pytest.raises(AttributeError):
        a.prop = 123


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
        a.prop = 123


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
        def prop(self) -> Any:
            """Docstring."""

    assert isinstance(A.prop, propcache_module.under_cached_property)
    assert "Docstring." == A.prop.__doc__
