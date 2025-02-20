"""codspeed benchmarks for propcache."""

import pytest

try:
    from pytest_codspeed import BenchmarkFixture
except ImportError:
    pytestmark = pytest.mark.skip("pytest_codspeed needs to be installed")

from propcache import cached_property, under_cached_property


def test_under_cached_property_cache_hit(benchmark: "BenchmarkFixture") -> None:
    """Benchmark for under_cached_property cache hit."""

    class Test:
        def __init__(self) -> None:
            self._cache = {"prop": 42}

        @under_cached_property
        def prop(self) -> int:
            """Return the value of the property."""
            raise NotImplementedError

    t = Test()

    @benchmark
    def _run() -> None:
        for _ in range(100):
            t.prop


def test_cached_property_cache_hit(benchmark: "BenchmarkFixture") -> None:
    """Benchmark for cached_property cache hit."""

    class Test:
        def __init__(self) -> None:
            self.__dict__["prop"] = 42

        @cached_property
        def prop(self) -> int:
            """Return the value of the property."""
            raise NotImplementedError

    t = Test()

    @benchmark
    def _run() -> None:
        for _ in range(100):
            t.prop


def test_under_cached_property_cache_miss(benchmark: "BenchmarkFixture") -> None:
    """Benchmark for under_cached_property cache miss."""

    class Test:
        def __init__(self) -> None:
            self._cache: dict[str, int] = {}

        @under_cached_property
        def prop(self) -> int:
            """Return the value of the property."""
            return 42

    t = Test()
    cache = t._cache

    @benchmark
    def _run() -> None:
        for _ in range(100):
            cache.pop("prop", None)
            t.prop


def test_cached_property_cache_miss(benchmark: "BenchmarkFixture") -> None:
    """Benchmark for cached_property cache miss."""

    class Test:

        @cached_property
        def prop(self) -> int:
            """Return the value of the property."""
            return 42

    t = Test()
    cache = t.__dict__

    @benchmark
    def _run() -> None:
        for _ in range(100):
            cache.pop("prop", None)
            t.prop
