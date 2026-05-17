"""Various helper functions."""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping
from functools import cached_property
from typing import Any, Generic, Protocol, TypeVar, overload

__all__ = (
    "under_cached_property",
    "under_cached_property_with_name",
    "under_cache_name",
    "cached_property",
)


if sys.version_info >= (3, 11):
    from typing import Self
else:
    Self = Any

_T = TypeVar("_T")
# We use Mapping to make it possible to use TypedDict, but this isn't
# technically type safe as we need to assign into the dict.
_Cache = TypeVar("_Cache", bound=Mapping[str, Any])


class _CacheImpl(Protocol[_Cache]):
    _cache: _Cache


class under_cached_property(Generic[_T]):
    """Use as a class method decorator.

    It operates almost exactly like
    the Python `@property` decorator, but it puts the result of the
    method it decorates into the instance dict after the first call,
    effectively replacing the function it decorates with an instance
    variable.  It is, in Python parlance, a data descriptor.
    """

    def __init__(self, wrapped: Callable[[Any], _T]) -> None:
        self.wrapped = wrapped
        self.__doc__ = wrapped.__doc__
        self.name = wrapped.__name__

    @overload
    def __get__(self, inst: None, owner: type[object] | None = None) -> Self: ...

    @overload
    def __get__(
        self, inst: _CacheImpl[Any], owner: type[object] | None = None
    ) -> _T: ...

    def __get__(
        self, inst: _CacheImpl[Any] | None, owner: type[object] | None = None
    ) -> _T | Self:
        if inst is None:
            return self
        try:
            return inst._cache[self.name]  # type: ignore[no-any-return]
        except KeyError:
            val = self.wrapped(inst)
            inst._cache[self.name] = val
            return val

    def __set__(self, inst: _CacheImpl[Any], value: _T) -> None:
        raise AttributeError("cached property is read-only")


class under_cached_property_with_name(Generic[_T]):
    """Like ``under_cached_property`` but reads the cache from a named attribute.

    The default ``under_cached_property`` always reads/writes ``inst._cache``.
    This variant lets the caller pick a different attribute name, which is
    useful for classes that use ``__slots__`` (where ``_cache`` would clash
    with a slot of the same name on subclasses), or for classes that want to
    partition cached values into multiple buckets.

    The named attribute must be a mutable mapping (typically a ``dict``)
    and must exist on the instance before the first attribute access.
    """

    def __init__(self, wrapped: Callable[[Any], _T], cache_name: str) -> None:
        self.wrapped = wrapped
        self.__doc__ = wrapped.__doc__
        self.name = wrapped.__name__
        self.cache_name = cache_name

    @overload
    def __get__(self, inst: None, owner: type[object] | None = None) -> Self: ...

    @overload
    def __get__(self, inst: object, owner: type[object] | None = None) -> _T: ...

    def __get__(
        self, inst: object | None, owner: type[object] | None = None
    ) -> _T | Self:
        if inst is None:
            return self
        cache: dict[str, Any] = getattr(inst, self.cache_name)
        try:
            return cache[self.name]  # type: ignore[no-any-return]
        except KeyError:
            val = self.wrapped(inst)
            cache[self.name] = val
            return val

    def __set__(self, inst: object, value: _T) -> None:
        raise AttributeError("cached property is read-only")


class under_cache_name:
    """Decorator factory binding a cache attribute name.

    Calling an instance with a function returns an
    ``under_cached_property_with_name`` configured to store its value in the
    pre-bound attribute. Useful for defining a project-wide ``reify`` alias
    once and reusing it across many class definitions::

        reify = under_cache_name("_my_cache")

        class MyTool:
            __slots__ = ("i", "_my_cache")

            def __init__(self, i: int) -> None:
                self.i = i
                self._my_cache = {}

            @reify
            def cached_item(self) -> int:
                return self.i + 10
    """

    def __init__(self, cache_name: str) -> None:
        self.cache_name = cache_name

    def __call__(
        self, wrapped: Callable[[Any], _T]
    ) -> under_cached_property_with_name[_T]:
        return under_cached_property_with_name(wrapped, self.cache_name)
