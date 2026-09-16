# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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

from abc import ABC
from typing import Optional

from dimp import Address, AddressFactory
from dimp import ANYWHERE, EVERYWHERE

from ..mem.ext import address_cache

from .address_btc import BTCAddress
from .address_eth import ETHAddress


class BaseAddressFactory(AddressFactory, ABC):
    """Base address factory.

    Parses address strings with cache, supporting
    broadcast addresses (anywhere/everywhere) and
    normal addresses (BTC/ETH/...).
    """

    # Override
    def parse_address(self, address: str) -> Optional[Address]:
        cache = address_cache()
        add = cache.get(key=address)
        if add is None:
            add = self._parse(address=address)
            if add is not None:
                cache.put(key=address, value=add)
        return add

    # noinspection PyMethodMayBeStatic
    def _parse(self, address: str) -> Optional[Address]:
        """Parse an address string.

        `address` is the string representation; returns an `Address`
        instance if the format is recognized, null otherwise.
        """
        size = len(address)
        #
        #  check broadcast address
        #
        if size == 8:
            # "anywhere"
            if address.lower() == 'anywhere':
                return ANYWHERE
        elif size == 10:
            # "everywhere"
            if address.lower() == 'everywhere':
                return EVERYWHERE
        #
        #  checking normal address
        #
        if 26 <= size <= 35:
            return BTCAddress.from_str(address=address)
        elif size == 42:
            return ETHAddress.from_str(address=address)
        #
        # TODO: other types of address
        #
        assert False, f'invalid address: {address}'
