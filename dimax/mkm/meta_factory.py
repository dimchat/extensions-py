# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
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

from dimp import StrMap
from dimp import TransportableData
from dimp import UTF8
from dimp import VerifyKey, SignKey, PrivateKey

from dimp import Address
from dimp import Meta, MetaFactory

from dimp import AccountHandler, GeneralAccountExtension
from dimp import shared_account_extensions

from ..protocol import MetaType

from .address_btc import BTCAddress
from .address_eth import ETHAddress
from .meta import BaseMeta


"""
    Default Meta to build ID with 'name@address'
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    version:
        1 - MKM

    algorithm:
        CT      = fingerprint = sKey.sign(seed);
        hash    = ripemd160(sha256(CT));
        code    = sha256(sha256(network + hash)).prefix(4);
        address = base58_encode(network + hash + code);
"""


class DefaultMeta(BaseMeta):

    @property  # Override
    def has_seed(self) -> bool:
        return True

    # Override
    def generate_address(self, network: int = None) -> Address:
        # assert self.type == 'MKM' or self.type == '1', f'meta version error: {self.type}'
        assert network is not None, 'address type should not be empty'
        # generate BTC address with fingerprint
        ted = self.fingerprint
        data = ted.to_bytes()
        return BTCAddress.from_data(data, network=network)


"""
    Meta to build BTC address for ID
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    version:
        2 - BTC

    algorithm:
        CT      = key.data;
        hash    = ripemd160(sha256(CT));
        code    = sha256(sha256(network + hash)).prefix(4);
        address = base58_encode(network + hash + code);
"""


class BTCMeta(BaseMeta):

    @property  # Override
    def has_seed(self) -> bool:
        return False

    # Override
    def generate_address(self, network: int = None) -> Address:
        # assert self.type == 'BTC' or self.type == '2', f'meta version error: {self.type}'
        assert network is not None, 'address type should not be empty'
        # generate BTC address with public key data
        key = self.public_key
        ted = key.data
        data = ted.to_bytes()
        return BTCAddress.from_data(data, network=network)


"""
    Meta to build ETH address for ID
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    version:
        4 - ETH

    algorithm:
        fingerprint = key.data
        digest      = keccak256(fingerprint)
        address     = hex_encode(digest.suffix(20))
"""


class ETHMeta(BaseMeta):

    @property  # Override
    def has_seed(self) -> bool:
        return False

    # Override
    def generate_address(self, network: int = None) -> Address:
        # assert self.type == 'ETH' or self.type == '4', f'meta version error: {self.type}'
        # generate ETH address with public key data
        key = self.public_key
        ted = key.data
        data = ted.to_bytes()
        return ETHAddress.from_data(data)


class BaseMetaFactory(MetaFactory):

    def __init__(self, version: str):
        super().__init__()
        self.__type = version

    @property  # protected
    def type(self) -> str:
        return self.__type

    # Override
    def generate_meta(self, private_key: SignKey, seed: Optional[str]) -> Meta:
        if seed is None or len(seed) == 0:
            fingerprint = None
        else:
            sig = private_key.sign(data=UTF8.encode(string=seed))
            fingerprint = TransportableData.create(data=sig)
        assert isinstance(private_key, PrivateKey), f'private key error: {private_key}'
        public_key = private_key.public_key
        return self.create_meta(public_key=public_key, seed=seed, fingerprint=fingerprint)

    # Override
    def create_meta(self, public_key: VerifyKey, seed: Optional[str], fingerprint: Optional[TransportableData]) -> Meta:
        version = self.type
        if version == MetaType.MKM:
            out = DefaultMeta(version=version, public_key=public_key, seed=seed, fingerprint=fingerprint)
        elif version == MetaType.BTC:
            out = BTCMeta(version=version, public_key=public_key)
        elif version == MetaType.ETH:
            out = ETHMeta(version=version, public_key=public_key)
        else:
            raise TypeError(f'unknown meta type: {version}')
        assert out.is_valid, f'meta error: {out}'
        return out

    # Override
    def parse_meta(self, meta: StrMap) -> Optional[Meta]:
        # check 'type', 'key', 'seed', 'fingerprint'
        if 'type' not in meta or 'key' not in meta:
            # meta.type should not be empty
            # meta.key should not be empty
            return None
        elif 'seed' not in meta:
            if 'fingerprint' in meta:
                assert False, f'meta error: {meta}'
        elif 'fingerprint' not in meta:
            assert False, f'meta error: {meta}'
        helper = doc_helper()
        version = helper.get_meta_type(meta=meta)
        if version == MetaType.MKM:
            out = DefaultMeta(meta=meta)
        elif version == MetaType.BTC:
            out = BTCMeta(meta=meta)
        elif version == MetaType.ETH:
            out = ETHMeta(meta=meta)
        else:
            raise TypeError(f'unknown meta type: {version}')
        if out.is_valid:
            return out
        # assert False, f'meta error: {meta}'


def account_extensions() -> GeneralAccountExtension:
    return shared_account_extensions


def doc_helper() -> AccountHandler:
    ext = account_extensions()
    return ext.handler
