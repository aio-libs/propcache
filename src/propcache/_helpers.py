import os
import sys
from typing import TYPE_CHECKING

__all__ = (
    "cached_property",
    "under_cached_property",
    "under_cached_property_with_name",
    "under_cache_name",
)


NO_EXTENSIONS = bool(os.environ.get("PROPCACHE_NO_EXTENSIONS"))  # type: bool
if sys.implementation.name != "cpython":
    NO_EXTENSIONS = True


# isort: off
if TYPE_CHECKING:
    from ._helpers_py import cached_property as cached_property_py
    from ._helpers_py import under_cache_name as under_cache_name_py
    from ._helpers_py import under_cached_property as under_cached_property_py
    from ._helpers_py import (
        under_cached_property_with_name as under_cached_property_with_name_py,
    )

    cached_property = cached_property_py
    under_cached_property = under_cached_property_py
    under_cached_property_with_name = under_cached_property_with_name_py
    under_cache_name = under_cache_name_py
elif not NO_EXTENSIONS:  # pragma: no branch
    try:
        from ._helpers_c import cached_property as cached_property_c  # type: ignore[attr-defined, unused-ignore]
        from ._helpers_c import under_cache_name as under_cache_name_c  # type: ignore[attr-defined, unused-ignore]
        from ._helpers_c import under_cached_property as under_cached_property_c  # type: ignore[attr-defined, unused-ignore]
        from ._helpers_c import under_cached_property_with_name as under_cached_property_with_name_c  # type: ignore[attr-defined, unused-ignore]

        cached_property = cached_property_c
        under_cached_property = under_cached_property_c
        under_cached_property_with_name = under_cached_property_with_name_c
        under_cache_name = under_cache_name_c
    except ImportError:  # pragma: no cover
        from ._helpers_py import cached_property as cached_property_py
        from ._helpers_py import under_cache_name as under_cache_name_py
        from ._helpers_py import under_cached_property as under_cached_property_py
        from ._helpers_py import (
            under_cached_property_with_name as under_cached_property_with_name_py,
        )

        cached_property = cached_property_py  # type: ignore[assignment, misc]
        under_cached_property = under_cached_property_py
        under_cached_property_with_name = under_cached_property_with_name_py
        under_cache_name = under_cache_name_py
else:
    from ._helpers_py import cached_property as cached_property_py
    from ._helpers_py import under_cache_name as under_cache_name_py
    from ._helpers_py import under_cached_property as under_cached_property_py
    from ._helpers_py import (
        under_cached_property_with_name as under_cached_property_with_name_py,
    )

    cached_property = cached_property_py  # type: ignore[assignment, misc]
    under_cached_property = under_cached_property_py
    under_cached_property_with_name = under_cached_property_with_name_py
    under_cache_name = under_cache_name_py
# isort: on
