"""Various helper functions."""

import sys
from collections.abc import Mapping
from functools import cached_property
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Protocol,
    TypeVar,
    Union,
    overload,
)

__all__ = ("CacheBase", "under_cached_property", "cached_property")


if sys.version_info >= (3, 11):
    from typing import Self
else:
    Self = Any

_T = TypeVar("_T")
# We use Mapping to make it possible to use TypedDict, but this isn't
# technically type safe as we need to assign into the dict.
_Cache = TypeVar("_Cache", bound=Mapping[str, Any])


class CacheBase:
    """Base class for objects that use cached properties.  This class
    provides a _cache attribute that is used to store the results of
    cached properties.

    Callers are responsible for calling super().__init__() in their
    __init__() methods to ensure that the _cache attribute is
    initialized.
    """

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}


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
    def __get__(self, inst: None, owner: Optional[type[object]] = None) -> Self: ...

    @overload
    def __get__(self, inst: _CacheImpl[Any], owner: Optional[type[object]] = None) -> _T: ...  # type: ignore[misc]

    def __get__(
        self, inst: Optional[_CacheImpl[Any]], owner: Optional[type[object]] = None
    ) -> Union[_T, Self]:
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
