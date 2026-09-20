# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2026 Albert Moky
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

from typing import Union

from dimp import ID, Address
from dimp import GeneralAccountExtension
from dimp import shared_account_extensions

from .cache import MemoryCache, ThanosCache


# -----------------------------------------------------------------------------
#  Memory Cache Extensions
# -----------------------------------------------------------------------------


class MemoryCacheExtension:
    """Memory cache extensions."""

    @property
    def address_cache(self) -> MemoryCache[str, Address]:
        """ Get address cache """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.address_cache getter'
        )

    @address_cache.setter
    def address_cache(self, cache: MemoryCache):
        """Set the address cache."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.address_cache setter'
        )

    @property
    def id_cache(self) -> MemoryCache[str, ID]:
        """ Get ID cache """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.id_cache getter'
        )

    @id_cache.setter
    def id_cache(self, cache: MemoryCache):
        """Set the ID cache."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.id_cache setter'
        )


shared_account_extensions.address_cache = ThanosCache()
shared_account_extensions.id_cache = ThanosCache()


def _account_extension() -> Union[MemoryCacheExtension, GeneralAccountExtension]:
    return shared_account_extensions


def address_cache() -> MemoryCache[str, Address]:
    ext = _account_extension()
    return ext.address_cache


def id_cache() -> MemoryCache[str, ID]:
    ext = _account_extension()
    return ext.id_cache


def reduce_memory() -> int:
    """ Call it when received 'UIApplicationDidReceiveMemoryWarningNotification',
        this will remove 50% of cached objects.

        Returns the number of survivors.
    """
    ext = _account_extension()
    cnt1 = ext.address_cache.reduce_memory()
    cnt2 = ext.id_cache.reduce_memory()
    return cnt1 + cnt2
