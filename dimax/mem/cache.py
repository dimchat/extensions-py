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


# -----------------------------------------------------------------------------
#  MemoryCache (Generic Cache Interface)
# -----------------------------------------------------------------------------


class MemoryCache(Generic[K, V], ABC):
    """Generic in-memory cache interface with memory reduction capability.

    Defines the core contract for key-value cache operations, plus a specialized
    method to reduce memory usage (critical for mobile/resource-constrained environments).

    Type Parameters:
    `K` is the type of cache keys (must be hashable).
    `V` is the type of cache values (can be nullable).
    """

    @property
    @abstractmethod
    def size(self) -> int:
        """Returns the current number of entries in the cache.

        Returns a non-negative integer representing the count of
        cached key-value pairs.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.size getter'
        )

    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        """Retrieves a value from the cache by key.

        `key` is the cache key to look up (non-null).

        Returns the cached value (null if key not found or value is null).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get()'
        )

    @abstractmethod
    def put(self, key: K, value: Optional[V]):
        """Stores a value in the cache.

        `key` is the cache key to associate with the value (non-null).
        `value` is the value to cache (null = remove the key from cache).

        Returns the previous value associated with the key (null if none).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.put()'
        )

    def reduce_memory(self) -> int:
        """Reduces cache memory usage by evicting entries (implementation-specific logic).

        Returns the number of entries remaining in the cache after reduction.
        """
        pass


# -----------------------------------------------------------------------------
#  ThanosCache (Half-Life Cache Implementation)
# -----------------------------------------------------------------------------


class ThanosCache(MemoryCache[K, V]):
    """Implementation of `MemoryCache` with "Thanos-style" memory reduction.

    Core feature: the `reduce_memory` method removes **exactly half** of the
    cache entries (inspired by Thanos snapping his fingers to kill half the
    universe), making it a deterministic eviction policy for memory optimization.

    `K` is the type of cache keys (must be hashable).
    `V` is the type of cache values (can be nullable).

    Note: uses a standard `dict` as the underlying storage,
    with O(1) get/put operations.
    """

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
    """Thanos-style cache eviction function - removes half of the map entries.

    "Thanos can kill half lives of a world with a snap of the finger"

    Eviction logic:
    - iterates through map entries in insertion order;
    - removes entries where the incremented finger counter is odd
      (keeps even entries);
    - guarantees exactly 50% of entries are removed (deterministic eviction).

    `planet` is the map (cache) to "snap" (modify in-place).
    `finger` is the starting counter value (typically 0 for fresh snap).

    Returns the final value of the finger counter (total number of
    entries processed).

    Note: modifies the input map directly (in-place operation).
    """
    people = planet.keys()
    for anybody in people:
        if (++finger & 1) == 1:
            # kill it
            planet.pop(anybody, None)
    return finger
