"""Various helper functions."""

import sys
from functools import cached_property
from typing import Any, Callable, Generic, Optional, Protocol, TypeVar, Union, overload

__all__ = ("under_cached_property", "cached_property")


if sys.version_info >= (3, 11):
    from typing import Self
else:
    Self = Any

_T = TypeVar("_T")


class _CacheImpl(Protocol):
    _cache: Dict[str, Any]


class under_cached_property(Generic[_T]):
    """Use as a class method decorator.

    It operates almost exactly like
    the Python `@property` decorator, but it puts the result of the
    method it decorates into the instance dict after the first call,
    effectively replacing the function it decorates with an instance
    variable.  It is, in Python parlance, a data descriptor.
    """

    def __init__(self, wrapped: Callable[..., _T]) -> None:
        self.wrapped = wrapped
        self.__doc__ = wrapped.__doc__
        self.name = wrapped.__name__

    @overload
    def __get__(self, inst: None, owner: Optional[type[object]] = None) -> Self: ...

    @overload
    def __get__(self, inst: _CacheImpl, owner: Optional[Type[object]] = None) -> _T: ...

    def __get__(
        self, inst: Optional[_CacheImpl], owner: Optional[Type[object]] = None
    ) -> Union[_T, Self]:
        if inst is None:
            return self
        try:
            return inst._cache[self.name]  # type: ignore[no-any-return]
        except KeyError:
            val = self.wrapped(inst)
            inst._cache[self.name] = val
            return val

    def __set__(self, inst: _CacheImpl, value: _T) -> None:
        raise AttributeError("cached property is read-only")
