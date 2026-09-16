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
from dimp import Converter

from dimp import ContentType
from dimp import Content, Envelope

from .base import BaseContent


class QuoteContent(Content, ABC):
    """Quote reply message content interface.

    Used to create "quote reply" messages that reference a previous message
    (the "original" message) with additional text commentary.

    JSON format:
    ```json
    {
      "type" : i2s(0x37),
      "sn"   : 67890,

      "text"   : "...",  // Reply text content
      "origin" : {       // Metadata of the original message being quoted
        "sender"   : "...",      // Sender ID of the original message
        "receiver" : "...",      // Receiver ID (or group ID) of the original message
        "type"     : i2s(0x01),  // Content type of the original message
        "sn"       : 12345       // Serial number of the original message
      }
    }
    ```
    """

    @property
    @abstractmethod
    def text(self) -> str:
        """Gets the reply text content of the quote message.

        This is the user's new commentary/response to the original quoted message.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.text getter'
        )

    @property
    @abstractmethod
    def original_envelope(self) -> Optional[Envelope]:
        """Gets the envelope of the original message being quoted.

        Contains sender/receiver/time metadata of the message being replied to.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.original_envelope getter'
        )

    @property
    @abstractmethod
    def original_sn(self) -> Optional[int]:
        """Gets the serial number (SN) of the original message being quoted.

        Unique identifier of the original message, used to locate it in conversation history.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.original_sn getter'
        )

    #
    #   Factory method
    #

    @classmethod
    def create(cls, text: str, envelope: Envelope, content: Content):
        """Creates a `QuoteContent` instance with reply text and original message metadata.

        Automatically purifies the original message's envelope/content using `QuoteHelper`
        to generate the "origin" field in the quote message.

        `text` is the user's reply text to the original message.
        `envelope` is the envelope of the original message being quoted.
        `content` is the content of the original message being quoted.

        Returns a new `QuoteContent` instance.

        :param text:     message text
        :param envelope: original message head
        :param content:  original message body
        :return: ReceiptCommand
        """
        source = envelope.sender
        target = content.group
        if target is None:
            target = envelope.receiver
        # build origin info
        origin = {
            'sender': str(source),
            'receiver': str(target),
            'type': content.type,
            'sn': content.sn,
        }
        return BaseQuoteContent(text=text, origin=origin)


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseQuoteContent(BaseContent, QuoteContent):

    def __init__(self, content: StrMap = None,
                 text: str = None, origin: StrMap = None):
        if content is None:
            # 1. new content with text & origin info
            assert not (text is None or origin is None), f'quote error: {text}, {origin}'
            msg_type = ContentType.QUOTE
            super().__init__(None, msg_type)
            self['text'] = text
            self['origin'] = origin
        else:
            # 2. content info from network
            assert text is None and origin is None, f'quote error: {text}, {origin}'
            super().__init__(content=content)
        # lazy load
        self.__env: Optional[Envelope] = None

    @property  # Override
    def text(self) -> str:
        return self.get_str(key='text', default='')

    @property  # protected
    def origin(self) -> Optional[StrMap]:
        return self.get('origin')

    @property  # Override
    def original_envelope(self) -> Optional[Envelope]:
        env = self.__env
        if env is None:
            # origin: { sender: "...", receiver: "...", time: 0 }
            env = Envelope.parse(envelope=self.origin)
            self.__env = env
        return env

    @property  # Override
    def original_sn(self) -> Optional[int]:
        origin = self.origin
        if origin is not None:
            sn = origin.get('sn')
            return Converter.get_int(value=sn)
