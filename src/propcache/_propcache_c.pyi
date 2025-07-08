from __future__ import annotations

import sys
from typing import Any, Callable, Generic, Mapping, Protocol, Type, TypeVar, overload

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

class cached_property(Generic[_T]):
    func: Callable[[Any], _T]
    name: str
    def __init__(self, func: Callable[[Any], _T]) -> None: ...
    @classmethod
    def __class_getitem__(cls, *args, **kwargs): ...
    def __get__(self, instance: _T, owner: Type[Any]) -> _T: ...
    def __set_name__(self, name: str, owner: Type[Any]): ...

class under_cached_property(Generic[_T]):
    name: str
    wrapped: Callable[[Any], _T]
    def __init__(self, wrapped: Callable[[Any], _T]) -> None: ...
    @classmethod
    def __class_getitem__(cls, *args, **kwargs): ...
    def __delete__(self, *args, **kwargs): ...
    @overload
    def __get__(self, inst: None, owner: type[object] | None = None) -> Self: ...
    @overload
    def __get__(self, inst: _CacheImpl[Any], owner: type[object] | None = None) -> _T: ...  # type: ignore[misc]
    def __get__(
        self, inst: _CacheImpl[Any] | None, owner: type[object] | None = None
    ): ...
    def __set__(self, inst: _CacheImpl[Any] | None, value: Any): ...
