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

from abc import ABC, abstractmethod
from typing import Optional

from dimp import StrMap
from dimp import Dictionary

from dimp import TransportableData
from dimp import UTF8
from dimp import VerifyKey, PublicKey
from dimp import Meta
from dimp import ID, Address
from dimp import AccountHandler
from dimp import GeneralAccountExtension, shared_account_extensions


"""
    User/Group Meta data
    ~~~~~~~~~~~~~~~~~~~~
    This class is used to generate entity ID

    data format: {
        "type"        : i2s(1),         // meta version
        "key"         : "{public key}", // PK = secp256k1(SK);
        "seed"        : "moKy",         // user/group name
        "fingerprint" : "..."           // CT = sign(seed, SK);
    }

    algorithm:
        fingerprint = sign(seed, SK);

    abstractmethod:
        - generate_address(network)
"""


class BaseMeta(Dictionary, Meta, ABC):

    def __init__(self, meta: StrMap = None,
                 version: str = None, public_key: VerifyKey = None,
                 seed: Optional[str] = None, fingerprint: Optional[TransportableData] = None):
        # check parameters
        if meta is not None:
            # 0. meta info from network
            assert version is None and public_key is None and seed is None and fingerprint is None, \
                f'params error: {meta}, {version}, {public_key}, {seed}, {fingerprint}'
            # waiting to verify
            # all metas must be verified before saving into local storage
            status = 0
        elif seed is None or fingerprint is None:
            # 1. new meta with type & public key only
            assert version is not None and public_key is not None, \
                f'meta info error: {version}, {public_key}, {seed}, {fingerprint}'
            assert seed is None and fingerprint is None, 'meta seed/fingerprint error'
            meta = {
                'type': version,
                'key': public_key.to_map(),
            }
            # generated meta, or loaded from local storage,
            # no need to verify again.
            status = 1
        else:
            # 2. new meta with type, public key, seed & fingerprint
            assert version is not None and public_key is not None, \
                f'meta info error: {version}, {public_key}, {seed}, {fingerprint}'
            meta = {
                'type': version,
                'key': public_key.to_map(),
                'seed': seed,
                'fingerprint': fingerprint.serialize(),
            }
            # generated meta, or loaded from local storage,
            # no need to verify again.
            status = 1
        # initialize with meta info
        super().__init__(dictionary=meta)
        # lazy load
        self.__type = version
        self.__key = public_key
        self.__seed = seed
        self.__fingerprint = fingerprint
        self.__status = status
        # caches
        self.__caches = {}

    @property  # Override
    def type(self) -> str:
        if self.__type is None:
            helper = account_handler()
            info = super().to_map()
            self.__type = helper.get_meta_type(meta=info, default='')
            # self.__type = self.get_int(key='type', default=0)
        return self.__type

    @property  # Override
    def public_key(self) -> VerifyKey:
        if self.__key is None:
            info = self.get('key')
            self.__key = PublicKey.parse(key=info)
            assert self.__key is not None, f'meta key error: {info}'
        return self.__key

    # protected
    @property
    @abstractmethod
    def has_seed(self) -> bool:
        # version = self.type
        # return version == 'MKM' or version == '1'
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.has_seed getter'
        )

    @property  # Override
    def seed(self) -> Optional[str]:
        if self.__seed is None and self.has_seed:
            self.__seed = self.get_str(key='seed', default='')
            assert self.__seed is not None, f'meta.seed empty: {self}'
        return self.__seed

    @property  # Override
    def fingerprint(self) -> Optional[TransportableData]:
        ted = self.__fingerprint
        if ted is None and self.has_seed:
            base64 = self.get('fingerprint')
            assert base64 is not None, 'meta.fingerprint should not be empty: %s' % super().to_map()
            self.__fingerprint = ted = TransportableData.parse(base64)
            assert ted is not None, f'meta.fingerprint error: {base64}'
        return ted

    #
    #   Validation
    #

    @property
    def is_valid(self) -> bool:
        if self.__status == 0:
            # meta from network, try to verify
            if self._check_valid():
                # correct
                self.__status = 1
            else:
                # error
                self.__status = -1
        return self.__status > 0

    # private
    def _check_valid(self) -> bool:
        key = self.public_key
        if key is None:
            return False
        elif self.has_seed:
            # check 'seed' & 'fingerprint'
            pass
        elif 'seed' in self.to_map() or 'fingerprint' in self.to_map():
            # this meta has no seed, so
            # it should not contains 'seed' or 'fingerprint'
            return False
        else:
            # this meta has no seed, so it's always valid
            # when the public key exists
            return True
        seed = self.seed
        fingerprint = self.fingerprint
        # check meta seed & signature
        if fingerprint is None or fingerprint.is_empty:
            # meta error
            return False
        elif seed is None or len(seed) == 0:
            # meta error
            return False
        # verify fingerprint
        data = UTF8.encode(string=seed)
        signature = fingerprint.to_bytes()
        if signature is None or len(signature) == 0:
            # TED error
            return False
        return key.verify(data=data, signature=signature)

    #
    #   Generation
    #

    @abstractmethod
    def generate_address(self, network: int = None) -> Address:
        """Generate address for the network.

        :param network: target network identifier (type)
        :return: an address instance for the given network
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.generate_address()'
        )

    def generate_id(self, network: int) -> ID:
        """Generate ID with address for network.

        The ID is built as 'name@address' where the address is
        generated by [generate_address] with the [network] type.

        :param network: target network identifier (type)
        :return: a new `ID` instance (without terminal)
        """
        did = self.__caches.get(network)
        if did is None:
            address = self.generate_address(network=network)
            assert address is not None and len(address) > 0,                 f'failed to generate ID: {network}, {self.to_map()}'
            did = ID.create(name=self.seed, address=address)
            self.__caches[network] = did
        return did


def account_extensions() -> GeneralAccountExtension:
    return shared_account_extensions


def account_handler() -> AccountHandler:
    ext = account_extensions()
    return ext.handler
