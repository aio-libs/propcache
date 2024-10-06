from types import ModuleType

import pytest


def test_under_cached_property(propcache_module: ModuleType) -> None:
    class A:
        def __init__(self):
            self._cache = {}

        @propcache_module.under_cached_property
        def prop(self):
            return 1

    a = A()
    assert a.prop == 1


def test_under_cached_property_class(propcache_module: ModuleType) -> None:
    class A:
        def __init__(self):
            """Init."""
            # self._cache not set because its never accessed in this test

        @propcache_module.under_cached_property
        def prop(self):
            """Docstring."""

    assert isinstance(A.prop, propcache_module.under_cached_property)
    assert A.prop.__doc__ == "Docstring."


def test_under_cached_property_assignment(propcache_module: ModuleType) -> None:
    class A:
        def __init__(self):
            self._cache = {}

        @propcache_module.under_cached_property
        def prop(self):
            """Mock property."""

    a = A()

    with pytest.raises(AttributeError):
        a.prop = 123


def test_under_cached_property_without_cache(propcache_module: ModuleType) -> None:
    class A:
        def __init__(self):
            pass

        @propcache_module.under_cached_property
        def prop(self):
            """Mock property."""

    a = A()

    with pytest.raises(AttributeError):
        a.prop = 123


def test_under_cached_property_check_without_cache(
    propcache_module: ModuleType,
) -> None:
    class A:
        def __init__(self):
            pass

        @propcache_module.under_cached_property
        def prop(self):
            """Mock property."""

    a = A()
    with pytest.raises(AttributeError):
        assert a.prop == 1


def test_under_cached_property_caching(propcache_module: ModuleType) -> None:

    class A:
        def __init__(self):
            self._cache = {}

        @propcache_module.under_cached_property
        def prop(self):
            """Docstring."""
            return 1

    a = A()
    assert 1 == a.prop


def test_under_cached_property_class_docstring(propcache_module: ModuleType) -> None:
    class A:
        def __init__(self):
            """Init."""

        @propcache_module.under_cached_property
        def prop(self):
            """Docstring."""

    assert isinstance(A.prop, propcache_module.under_cached_property)
    assert "Docstring." == A.prop.__doc__
