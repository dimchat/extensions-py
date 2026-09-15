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

from typing import List

from dimp import StrMap, MutableStrMap

from dimp import ReliableMessage
from dimp import ContentType

from ..protocol import ForwardContent
from ..protocol.base import BaseContent


class SecretContent(BaseContent, ForwardContent):

    def __init__(self, content: StrMap = None,
                 messages: List[ReliableMessage] = None):
        if content is None:
            # 1. new content with message(s)
            msg_type = ContentType.FORWARD
            super().__init__(None, msg_type)
            # if messages is not None:
            #     self['secrets'] = ReliableMessage.revert(messages=messages)
        else:
            # 2. content info from network
            assert messages is None, f'params error: {content}, {messages}'
            super().__init__(content)
        # lazy
        self.__secrets = messages

    # Override
    def to_map(self) -> MutableStrMap:
        # serialize top-secret messages
        messages = self.__secrets
        if messages is not None and self.get('secrets') is None:
            self['secrets'] = ReliableMessage.revert(messages=messages)
        # OK
        return super().to_map()

    @property  # Override
    def secrets(self) -> List[ReliableMessage]:
        messages = self.__secrets
        if messages is None:
            info = self.get('secrets')
            if isinstance(info, list):
                # get from 'secrets'
                messages = ReliableMessage.convert(array=info)
            else:
                assert info is None, f'secret messages error: {info}'
                # get from 'forward'
                forward = self.get('forward')
                msg = ReliableMessage.parse(msg=forward)
                if msg is None:
                    messages = []
                else:
                    messages = [msg]
            self.__secrets = messages
        return messages
