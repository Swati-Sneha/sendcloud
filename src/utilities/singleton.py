"""Pythonic Singleton pattern."""

from __future__ import annotations

from typing import Any, Generic, TypeVar, Optional

SingletonMetaType = TypeVar("SingletonMetaType", bound="SingletonMeta")


class SingletonMeta(type, Generic[SingletonMetaType]):
    _instance: Optional[SingletonMetaType] = None

    def __call__(cls: SingletonMetaType, *args: Any, **kwargs: Any) -> SingletonMetaType:
        if cls._instance is None:
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class Singleton(metaclass=SingletonMeta):
    """
    Extend this class to make your class a Singleton.

    By extending this class, there can be only one of it at a time, any
    subsequent attempt at instantiating the class will return the previously
    instantiated class.
    """

    _instance: Optional[Singleton] = None
