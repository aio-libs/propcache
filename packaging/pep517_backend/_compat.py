"""Cross-python stdlib shims."""

import os
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

# isort: off
if sys.version_info >= (3, 11):
    from contextlib import chdir as chdir_cm
    from tomllib import loads as load_toml_from_string
else:
    from tomli import loads as load_toml_from_string

    @contextmanager
    def chdir_cm(path: os.PathLike) -> Iterator[None]:
        """Temporarily change the current directory, recovering on exit."""
        original_wd = Path.cwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(original_wd)


# isort: on
__all__ = ("chdir_cm", "load_toml_from_string")  # noqa: WPS410
