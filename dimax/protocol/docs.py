# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
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

from dimp import TransportableFile
from dimp import EncryptKey

from dimp import ID
from dimp import Document


class Visa(Document, ABC):
    """User Visa document interface (user-specific authorization document).

    Defines a user's public-facing information and authorization keys, used for:
    - Generating temporary asymmetric keys for secure messaging
    - Authorizing third-party apps to log in
    """

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """Gets the user's display name/nickname.

        :return: user name
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.name getter'
        )

    @name.setter
    @abstractmethod
    def name(self, nickname: str):
        """Sets the user's display name/nickname.

        `nickname` is the new display name for the user.
        Set the user nickname.

        :param nickname: user name
        :return:
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.name setter'
        )

    @property
    @abstractmethod
    def public_key(self) -> Optional[EncryptKey]:
        """Gets the user's public encryption key.

        This key is used by other users to encrypt messages sent to this user.

        :return: public key
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.public_key getter'
        )

    @public_key.setter
    @abstractmethod
    def public_key(self, key: EncryptKey):
        """Sets the user's public encryption key.

        `key` is the new public key for message encryption.

        Set the public key for encryption.

        :param key: public key as visa.key
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.public_key setter'
        )

    @property
    @abstractmethod
    def avatar(self) -> Optional[TransportableFile]:
        """Gets the user's avatar image (URL/Base64).

        Returns a `TransportableFile` containing the avatar's URL or Base64 data.

        :return: PNF(URL)
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.avatar getter'
        )

    @avatar.setter
    @abstractmethod
    def avatar(self, url: TransportableFile):
        """Sets the user's avatar image (URL/Base64).

        `url` is the new avatar image (URL/Base64).

        Set the avatar image.

        :param url: PNF(URL)
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.avatar setter'
        )


class Bulletin(Document, ABC):
    """Group Bulletin document interface (group-specific announcement document).

    Defines a group's public-facing information and core attributes.
    """

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """Gets the group's display name/title.

        :return: group name
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.name getter'
        )

    @name.setter
    @abstractmethod
    def name(self, title: str):
        """Sets the group's display name/title.

        `title` is the new title for the group.

        Set the group name.

        :param title: group name
        :return:
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.name setter'
        )

    @property
    @abstractmethod
    def founder(self) -> Optional[ID]:
        """Gets the group founder's user ID.

        Identifies the original creator of the group.

        :return: user ID
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.founder getter'
        )
