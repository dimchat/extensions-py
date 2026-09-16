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

from typing import Optional

from dimp import Address
from dimp import ID, IDFactory
from dimp import Identifier

from ..mem.ext import id_cache


class GeneralIdentifierFactory(IDFactory):
    """General ID factory.

    Creates/parses entity IDs with cache, concatenating
    the name, address and terminal components.
    """

    # Override
    def create_id(self, name: Optional[str], address: Address, terminal: Optional[str]) -> ID:
        identifier = Identifier.concat(name=name, address=address, terminal=terminal)
        cache = id_cache()
        did = cache.get(key=identifier)
        if did is None:
            did = self._new_id(identifier=identifier, name=name, address=address, terminal=terminal)
            cache.put(key=identifier, value=did)
        return did

    # Override
    def parse_id(self, identifier: str) -> Optional[ID]:
        cache = id_cache()
        did = cache.get(key=identifier)
        if did is None:
            did = self._parse(identifier=identifier)
            if did is not None:
                cache.put(key=identifier, value=did)
        return did

    # noinspection PyMethodMayBeStatic
    def _new_id(self, identifier: str, name: Optional[str], address: Address, terminal: Optional[str]) -> ID:
        """Create a new `ID` instance.

        `identifier` is the full string form; `name` is the entity name;
        `address` is the core address; `terminal` is the terminal/location.

        Override this method for customized ID implementations.
        """
        return Identifier(identifier=identifier, name=name, address=address, terminal=terminal)

    def _parse(self, identifier: str) -> Optional[ID]:
        """Parse an ID string.

        `identifier` is in "name@address[/terminal]" format;
        returns an `ID` instance if parsing succeeds, null otherwise.
        """
        # split for "terminal"
        pair = identifier.split('/')
        cnt = len(pair)
        terminal = None if cnt == 1 else pair[1]
        # split for "name" @ "address"
        pair = pair[0].split('@')
        cnt = len(pair)
        name = None if cnt == 1 else pair[0]
        address = Address.parse(address=pair[cnt-1])
        # done
        if address is not None:
            return self._new_id(identifier=identifier, name=name, address=address, terminal=terminal)
        else:
            assert False, f'ID error: {identifier}'
