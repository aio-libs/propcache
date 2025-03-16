import sys
from collections.abc import Callable
from operator import not_
from typing import Protocol, TypeVar, TYPE_CHECKING

import pytest

from propcache.api import cached_property

if sys.version_info >= (3, 11):
    from typing import assert_type

_T = TypeVar("_T")


class APIProtocol(Protocol):
    # TODO: Check functools.cached_property signature.
    def cached_property(self, func: Callable[..., _T]) -> cached_property[_T]:
        ...


def test_cached_property(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            """Init."""

        @propcache_module.cached_property
        def prop(self) -> int:
            return 1

    a = A()
    assert a.prop == 1


def test_cached_property_without_cache(propcache_module: APIProtocol) -> None:
    class A:

        __slots__ = ()

        def __init__(self) -> None:
            pass

        @propcache_module.cached_property
        def prop(self) -> None:
            """Mock property."""

    a = A()

    with pytest.raises(AttributeError):
        a.prop = 123  # type: ignore[assignment]


def test_cached_property_check_without_cache(propcache_module: APIProtocol) -> None:
    class A:

        __slots__ = ()

        def __init__(self) -> None:
            """Init."""

        @propcache_module.cached_property
        def prop(self) -> None:
            """Mock property."""

    a = A()
    with pytest.raises((TypeError, AttributeError)):
        assert a.prop == 1


def test_cached_property_caching(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            """Init."""

        @propcache_module.cached_property
        def prop(self) -> int:
            """Docstring."""
            return 1

    a = A()
    assert a.prop == 1


def test_cached_property_class_docstring(propcache_module: APIProtocol) -> None:
    class A:
        def __init__(self) -> None:
            """Init."""

        @propcache_module.cached_property
        def prop(self) -> None:
            """Docstring."""

    if TYPE_CHECKING:
        assert isinstance(A.prop, cached_property)
    else:
        assert isinstance(A.prop, propcache_module.cached_property)
    assert "Docstring." == A.prop.__doc__


def test_set_name(propcache_module: APIProtocol) -> None:
    """Test that the __set_name__ method is called and checked."""

    class A:

        @propcache_module.cached_property
        def prop(self) -> None:
            """Docstring."""

    A.prop.__set_name__(A, "prop")

    match = r"Cannot assign the same cached_property to two "
    with pytest.raises(TypeError, match=match):
        A.prop.__set_name__(A, "something_else")


def test_get_without_set_name(propcache_module: APIProtocol) -> None:
    """Test that get without __set_name__ fails."""
    cp = propcache_module.cached_property(not_)

    class A:
        """A class."""

    A.cp = cp  # type: ignore[attr-defined]
    match = r"Cannot use cached_property instance "
    with pytest.raises(TypeError, match=match):
        _ = A().cp  # type: ignore[attr-defined]


def test_ensured_wrapped_function_is_accessible(propcache_module: APIProtocol) -> None:
    """Test that the wrapped function can be accessed from python."""

    class A:
        def __init__(self) -> None:
            """Init."""

        @propcache_module.cached_property
        def prop(self) -> int:
            """Docstring."""
            return 1

    a = A()
    assert A.prop.func(a) == 1
