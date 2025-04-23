import os
import sys
from typing import TYPE_CHECKING

__all__ = ("base_cached_property", "cached_property", "under_cached_property")


NO_EXTENSIONS = bool(os.environ.get("PROPCACHE_NO_EXTENSIONS"))  # type: bool
if sys.implementation.name != "cpython":
    NO_EXTENSIONS = True


# isort: off
if TYPE_CHECKING:
    from ._helpers_py import under_cached_property as base_cached_property_py
    from ._helpers_py import cached_property as cached_property_py
    from ._helpers_py import under_cached_property as under_cached_property_py
    from ._helpers_py import CacheBase as CacheBase_py

    base_cached_property = under_cached_property_py
    cached_property = cached_property_py
    under_cached_property = under_cached_property_py
    CacheBase = CacheBase_py
elif not NO_EXTENSIONS:  # pragma: no branch
    try:
        from ._helpers_c import base_cached_property as base_cached_property_c  # type: ignore[attr-defined, unused-ignore]
        from ._helpers_c import cached_property as cached_property_c  # type: ignore[attr-defined, unused-ignore]
        from ._helpers_c import under_cached_property as under_cached_property_c  # type: ignore[attr-defined, unused-ignore]
        from ._helpers_c import CacheBase as CacheBase_c  # type: ignore[attr-defined, unused-ignore]

        base_cached_property = base_cached_property_c
        cached_property = cached_property_c
        under_cached_property = under_cached_property_c
        CacheBase = CacheBase_c
    except ImportError:  # pragma: no cover
        from ._helpers_py import under_cached_property as base_cached_property_py
        from ._helpers_py import cached_property as cached_property_py
        from ._helpers_py import under_cached_property as under_cached_property_py
        from ._helpers_py import CacheBase as CacheBase_py

        base_cached_property = base_cached_property_py
        cached_property = cached_property_py  # type: ignore[assignment, misc]
        under_cached_property = under_cached_property_py
        CacheBase = CacheBase_py
else:
    from ._helpers_py import under_cached_property as base_cached_property_py
    from ._helpers_py import cached_property as cached_property_py
    from ._helpers_py import under_cached_property as under_cached_property_py
    from ._helpers_py import CacheBase as CacheBase_py

    base_cached_property = base_cached_property_py
    cached_property = cached_property_py  # type: ignore[assignment, misc]
    under_cached_property = under_cached_property_py
    CacheBase = CacheBase_py
# isort: on
