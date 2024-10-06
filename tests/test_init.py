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


@pytest.mark.parametrize(
    "prop_name",
    ("cached_property", "under_cached_property"),
)
@pytest.mark.parametrize(
    "api_list", (dir(propcache), propcache.__all__), ids=("dir", "__all__")
)
def test_public_api_is_in_inspectable_object_lists(prop_name, api_list):
    """Verify the public API is discoverable programmatically.

    This checks for presence of known public decorators module's
    ``__all__`` and ``dir()``.
    """
    assert prop_name in api_list


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
