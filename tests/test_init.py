"""Test imports can happen from top-level."""

import propcache
from propcache import _helpers


def test_api_at_top_level():
    """Verify the public API is accessible at top-level."""
    assert propcache.cached_property is not None
    assert propcache.under_cached_property is not None
    assert propcache.cached_property is _helpers.cached_property
    assert propcache.under_cached_property is _helpers.under_cached_property
