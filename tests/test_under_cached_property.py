import platform

import pytest

from propcache import _helpers, _helpers_py
from propcache._helpers import under_cached_property

IS_PYPY = platform.python_implementation() == "PyPy"


class CachedPropertyMixin:
    under_cached_property = NotImplemented

    def test_under_cached_property(self) -> None:
        class A:
            def __init__(self):
                self._cache = {}

            @self.under_cached_property  # type: ignore[misc]
            def prop(self):
                return 1

        a = A()
        assert a.prop == 1

    def test_under_cached_property_class(self) -> None:
        class A:
            def __init__(self):
                """Init."""
                # self._cache not set because its never accessed in this test

            @self.under_cached_property  # type: ignore[misc]
            def prop(self):
                """Docstring."""

        assert isinstance(A.prop, self.under_cached_property)
        assert A.prop.__doc__ == "Docstring."

    def test_under_cached_property_assignment(self) -> None:
        class A:
            def __init__(self):
                self._cache = {}

            @self.under_cached_property  # type: ignore[misc]
            def prop(self):
                """Mock property."""

        a = A()

        with pytest.raises(AttributeError):
            a.prop = 123

    def test_under_cached_property_without_cache(self) -> None:
        class A:
            def __init__(self):
                pass

            @self.under_cached_property  # type: ignore[misc]
            def prop(self):
                """Mock property."""

        a = A()

        with pytest.raises(AttributeError):
            a.prop = 123

    def test_under_cached_property_check_without_cache(self) -> None:
        class A:
            def __init__(self):
                pass

            @self.under_cached_property  # type: ignore[misc]
            def prop(self):
                """Mock property."""

        a = A()
        with pytest.raises(AttributeError):
            assert a.prop == 1


class A:
    def __init__(self):
        self._cache = {}

    @under_cached_property
    def prop(self):
        """Docstring."""
        return 1


def test_under_cached_property():
    a = A()
    assert 1 == a.prop


def test_under_cached_property_class():
    assert isinstance(A.prop, under_cached_property)
    assert "Docstring." == A.prop.__doc__


def test_under_cached_property_assignment():
    a = A()

    with pytest.raises(AttributeError):
        a.prop = 123


class TestPyCachedProperty(CachedPropertyMixin):
    under_cached_property = _helpers_py.under_cached_property  # type: ignore[assignment] # noqa: E501


if (
    not _helpers.NO_EXTENSIONS
    and not IS_PYPY
    and hasattr(_helpers, "under_cached_property_c")
):

    class TestCCachedProperty(CachedPropertyMixin):
        under_cached_property = _helpers.under_cached_property_c  # type: ignore[assignment, attr-defined, unused-ignore] # noqa: E501
