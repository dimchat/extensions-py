# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from typing import TypeVar, Generic
from typing import Optional


K = TypeVar('K')
V = TypeVar('V')


class MemoryCache(Generic[K, V], ABC):

    @property
    @abstractmethod
    def size(self) -> int:
        """ Get cached size """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.size getter'
        )

    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        """ Get cached value for key """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get()'
        )

    @abstractmethod
    def put(self, key: K, value: Optional[V]):
        """ Cache value for key """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.put()'
        )

    def reduce_memory(self) -> int:
        """ Garbage Collection """
        pass


class ThanosCache(MemoryCache[K, V]):

    def __init__(self):
        super().__init__()
        self.__caches = {}

    @property  # Override
    def size(self) -> int:
        return len(self.__caches)

    # Override
    def get(self, key: K) -> Optional[V]:
        return self.__caches.get(key)

    # Override
    def put(self, key: K, value: Optional[V]):
        if value is None:
            self.__caches.pop(key, None)
        else:
            self.__caches[key] = value

    # Override
    def reduce_memory(self) -> int:
        finger = 0
        finger = thanos(self.__caches, finger)
        return finger >> 1


def thanos(planet: MutableMapping, finger: int) -> int:
    """ Thanos can kill half lives of a world with a snap of the finger """
    people = planet.keys()
    for anybody in people:
        if (++finger & 1) == 1:
            # kill it
            planet.pop(anybody, None)
    return finger
