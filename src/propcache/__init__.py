"""propcache: An accelerated property cache for Python classes."""

from typing import TYPE_CHECKING, List

__version__ = "0.2.0.dev0"

# Imports have moved to `propcache.api` in 0.2.0+.
# This module is now a facade for the API.
if TYPE_CHECKING:
    from .api import cached_property, under_cached_property

__all__ = ("cached_property", "under_cached_property")


def _import_facade(attr: str) -> object:
    """Import the public API from the `api` module."""
    if attr in __all__:
        from . import api  # pylint: disable=import-outside-toplevel

        return getattr(api, attr)
    raise AttributeError(f"module 'propcache' has no attribute '{attr}'")


def _dir_facade() -> List[str]:
    """Include the public API in the module's dir() output."""
    return [*__all__, *globals().keys()]


__getattr__ = _import_facade
__dir__ = _dir_facade
