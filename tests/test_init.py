"""Test imports can happen from top-level."""

import pytest

import propcache
from propcache import _helpers


def test_api_at_top_level():
    """Verify the public API is accessible at top-level."""
    assert propcache.cached_property is not None
    assert propcache.under_cached_property is not None
    assert propcache.cached_property is _helpers.cached_property
    assert propcache.under_cached_property is _helpers.under_cached_property


def test_public_api_is_in_dir():
    """Verify the public API is accessible in the module's dir()."""
    assert "cached_property" in dir(propcache)
    assert "under_cached_property" in dir(propcache)


def test_public_api_is_in_all():
    """Verify the public API is accessible in the module's __all__."""
    assert "cached_property" in propcache.__all__
    assert "under_cached_property" in propcache.__all__


def test_importing_invalid_attr_raises():
    """Verify importing an invalid attribute raises an AttributeError."""
    match = r"^module 'propcache' has no attribute 'invalid_attr'$"
    with pytest.raises(AttributeError, match=match):
        propcache.invalid_attr


def test_import_error_invalid_attr():
    """Verify importing an invalid attribute raises an ImportError."""
    # No match here because the error is raised by the import system
    # and may vary between Python versions.
    with pytest.raises(ImportError):
        from propcache import invalid_attr  # noqa: F401
