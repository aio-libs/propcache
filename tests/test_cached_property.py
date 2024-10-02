import platform

import pytest

from propcache import _helpers, _helpers_py
from propcache._helpers import cached_property

IS_PYPY = platform.python_implementation() == "PyPy"


class CachedPropertyMixin:
    cached_property = NotImplemented

    def test_cached_property(self) -> None:
        class A:
            def __init__(self):
                self._cache = {}

            @self.cached_property  # type: ignore[misc]
            def prop(self):
                return 1

        a = A()
        assert a.prop == 1

    def test_cached_property_class(self) -> None:
        class A:
            def __init__(self):
                """Init."""
                # self._cache not set because its never accessed in this test

            @self.cached_property  # type: ignore[misc]
            def prop(self):
                """Docstring."""

        assert isinstance(A.prop, self.cached_property)
        assert A.prop.__doc__ == "Docstring."

    def test_cached_property_without_cache(self) -> None:
        class A:

            __slots__ = ()

            def __init__(self):
                pass

            @self.cached_property  # type: ignore[misc]
            def prop(self):
                """Mock property."""

        a = A()

        with pytest.raises(AttributeError):
            a.prop = 123

    def test_cached_property_check_without_cache(self) -> None:
        class A:

            __slots__ = ()

            def __init__(self):
                pass

            @self.cached_property  # type: ignore[misc]
            def prop(self):
                """Mock property."""

        a = A()
        with pytest.raises((TypeError, AttributeError)):
            assert a.prop == 1


class A:
    def __init__(self):
        self._cache = {}

    @cached_property
    def prop(self):
        """Docstring."""
        return 1


def test_cached_property():
    a = A()
    assert 1 == a.prop


def test_cached_property_class():
    assert isinstance(A.prop, cached_property)
    assert "Docstring." == A.prop.__doc__


class TestPyCachedProperty(CachedPropertyMixin):
    cached_property = _helpers_py.cached_property  # type: ignore[assignment]


if (
    not _helpers.NO_EXTENSIONS
    and not IS_PYPY
    and hasattr(_helpers, "cached_property_c")
):

    class TestCCachedProperty(CachedPropertyMixin):
        cached_property = _helpers.cached_property_c  # type: ignore[assignment, attr-defined, unused-ignore] # noqa: E501
