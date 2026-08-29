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
from dimp import GeneralAccountHelper
from dimp import GeneralAccountExtension, shared_account_extensions

from .cache import MemoryCache, ThanosCache


def account_helper() -> GeneralAccountHelper:
    ext = account_extensions()
    return ext.helper


# -----------------------------------------------------------------------------
#  Memory Cache Extensions
# -----------------------------------------------------------------------------


class MemoryCacheExtension:

    @property
    def address_cache(self) -> MemoryCache[str, Address]:
        """ Get address cache """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.address_cache getter'
        )

    @address_cache.setter
    def address_cache(self, cache: MemoryCache):
        """ Set address cache """
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
        """ Set ID cache """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.id_cache setter'
        )


shared_account_extensions.address_cache = ThanosCache()
shared_account_extensions.id_cache = ThanosCache()


def account_extensions() -> Union[MemoryCacheExtension, GeneralAccountExtension]:
    return shared_account_extensions


def address_cache() -> MemoryCache[str, Address]:
    ext = account_extensions()
    return ext.address_cache


def id_cache() -> MemoryCache[str, ID]:
    ext = account_extensions()
    return ext.id_cache
