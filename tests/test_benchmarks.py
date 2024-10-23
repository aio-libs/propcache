"""codspeed benchmarks for propcache."""

from pytest_codspeed import BenchmarkFixture  # type: ignore[import-untyped]

from propcache import cached_property, under_cached_property


def test_under_cached_property_caching(benchmark: BenchmarkFixture) -> None:
    """Benchmark for under_cached_property caching."""

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


def test_cached_property_caching(benchmark: BenchmarkFixture) -> None:
    """Benchmark for cached_property caching."""

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
