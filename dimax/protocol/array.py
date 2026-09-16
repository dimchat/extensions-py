# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
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
from typing import List

from dimp import StrMap, MutableStrMap
from dimp import Content
from dimp import ContentType

from .base import BaseContent


class ArrayContent(Content, ABC):
    """Content array interface for sending multiple contents in one message.

    Enables packaging multiple different types of `Content` into a single message.

    JSON format:
    ```json
    {
      "type" : i2s(0xCA),
      "sn"   : 12345,

      "contents" : [...]  // Array of different content types
    }
    ```
    """

    @property
    @abstractmethod
    def contents(self) -> List[Content]:
        """Array of multiple message contents (can be different types)."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.contents getter'
        )

    #
    #   Factory
    #
    @classmethod
    def create(cls, contents: List[Content]):
        return ListContent(contents=contents)


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class ListContent(BaseContent, ArrayContent):

    def __init__(self, content: StrMap = None, contents: List[Content] = None):
        if content is None:
            # 1. new content with a list
            assert contents is not None, 'content list should no be None'
            msg_type = ContentType.ARRAY
            super().__init__(None, msg_type)
            # if contents is not None:
            #     self['contents'] = Content.revert(contents=contents)
        else:
            # 2. content info from network
            assert contents is None, f'params error: {content}, {contents}'
            super().__init__(content)
        # lazy
        self.__list = contents

    # Override
    def to_map(self) -> MutableStrMap:
        # serialize message contents
        contents = self.__list
        if contents is not None and self.get('contents') is None:
            self['contents'] = Content.revert(contents=contents)
        # OK
        return super().to_map()

    @property  # Override
    def contents(self) -> List[Content]:
        array = self.__list
        if array is None:
            info = self.get('contents')
            if isinstance(info, list):
                array = Content.convert(array=info)
            else:
                array = []
            self.__list = array
        # OK
        return array
