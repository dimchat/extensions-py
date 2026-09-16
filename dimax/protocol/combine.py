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
from typing import List

from dimp import StrMap, MutableStrMap

from dimp import ContentType
from dimp import Content
from dimp import InstantMessage

from .base import BaseContent


class CombineContent(Content, ABC):
    """Combined forward content for chat history forwarding.

    Special message format designed to forward a set of chat records as a single message.

    JSON format:
    ```json
    {
      "type" : i2s(0xCF),
      "sn"   : 67890,

      "title"    : "...",  // Chat history title
      "messages" : [...]   // List of chat records to forward
    }
    ```
    """

    @property
    @abstractmethod
    def title(self) -> str:
        """Title for the forwarded chat history set."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.title getter'
        )

    @property
    @abstractmethod
    def messages(self) -> List[InstantMessage]:
        """List of chat records (instant messages) to be forwarded."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.messages getter'
        )

    #
    #   Factory methods
    #
    @classmethod
    def create(cls, title: str, messages: List[InstantMessage]):
        return CombineForwardContent(title=title, messages=messages)


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class CombineForwardContent(BaseContent, CombineContent):

    def __init__(self, content: StrMap = None,
                 title: str = None, messages: List[InstantMessage] = None):
        if content is None:
            # 1. new content with message(s)
            assert not (title is None or messages is None), f'params error: {title}, {messages}'
            msg_type = ContentType.COMBINE_FORWARD
            super().__init__(None, msg_type)
            self['title'] = title
            # if messages is not None:
            #     self['messages'] = InstantMessage.revert(messages=messages)
        else:
            # 2. content info from network
            assert title is None and messages is None, f'params error: {title}, {messages}'
            super().__init__(content)
        # lazy
        self.__history = messages

    # Override
    def to_map(self) -> MutableStrMap:
        # serialize history messages
        messages = self.__history
        if messages is not None and self.get('messages') is None:
            self['messages'] = InstantMessage.revert(messages=messages)
        # OK
        return super().to_map()

    @property  # Override
    def title(self) -> str:
        return self.get_str(key='title', default='')

    @property  # Override
    def messages(self) -> List[InstantMessage]:
        array = self.__history
        if array is None:
            info = self.get('messages')
            if isinstance(info, list):
                array = InstantMessage.convert(array=info)
            else:
                assert info is None, f'combined messages error: {info}'
                array = []
            self.__history = array
        return array
