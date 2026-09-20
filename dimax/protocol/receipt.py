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

"""
    Receipt Protocol
    ~~~~~~~~~~~~~~~~

    As receipt returned to sender to proofing the message's received
"""

from abc import ABC, abstractmethod
from typing import Optional

from dimp import StrMap
from dimp import Converter

from dimp import Envelope, Content
from dimp import Command
from dimp import command_handler

from .base import BaseCommand


class ReceiptCommand(Command, ABC):
    """Receipt command interface (message acknowledgment/receipt).

    Used to send receipt/acknowledgment for a previously received message,
    confirming delivery or providing status feedback (via text).

    JSON format:
    ```json
    {
      "type" : i2s(0x88),
      "sn"   : 67890,

      "command": "receipt",  // Fixed command name for receipt messages

      "text"   : "...",      // Receipt comment/feedback text
      "origin" : {           // Metadata of the original message being acknowledged
        "sender"   : "...",  // Sender ID of the original message
        "receiver" : "...",  // Receiver ID of the original message
        "time"     : 123.45, // Timestamp of the original message
        "sn"       : 12345,  // Serial number of the original message
        "signature": "..."   // Signature of the original message (for verification)
      }
    }
    ```
    """

    RECEIPT = 'receipt'  # message receipt/acknowledgment

    @property
    @abstractmethod
    def text(self) -> str:
        """Gets the receipt comment/feedback text.

        Can be used to provide status info (e.g., "Message read", "Delivery failed")
        or custom feedback about the original message.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.text getter'
        )

    @property
    @abstractmethod
    def original_envelope(self) -> Optional[Envelope]:
        """Gets the envelope of the original message being acknowledged.

        Contains sender/receiver/time metadata of the message being receipted.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.original_envelope getter'
        )

    @property
    @abstractmethod
    def original_sn(self) -> Optional[int]:
        """Gets the serial number (SN) of the original message being acknowledged.

        Unique identifier of the original message, used to locate it in conversation history.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.original_sn getter'
        )

    @property
    @abstractmethod
    def original_signature(self) -> Optional[str]:
        """Gets the digital signature of the original message being acknowledged.

        Used to verify the authenticity of the original message in the receipt.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.original_signature getter'
        )

    #
    #   Factory method
    #

    @classmethod
    def create(cls, text: str, envelope: Envelope, content: Content = None):
        """Creates a `ReceiptCommand` instance with receipt text and original message metadata.

        Automatically purifies the original message's envelope/content using `QuoteHelper`
        to generate the "origin" field (removes sensitive data). Also handles group message
        receipt by setting the group ID if present in the original content.

        `text` is the receipt comment/feedback text.
        `envelope` is the optional envelope of the original message being acknowledged.
        `content` is the optional content of the original message being acknowledged.

        Returns a new `ReceiptCommand` instance.

        :param text:     message text
        :param envelope: original message head
        :param content:  original message body
        :return: ReceiptCommand
        """
        helper = command_handler()
        content = helper.create_receipt(text=text, envelope=envelope, content=content)
        if isinstance(content, ReceiptCommand):
            return content
        assert False, f'invalid receipt: {content}'


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseReceiptCommand(BaseCommand, ReceiptCommand):

    def __init__(self, content: StrMap = None,
                 text: str = None, origin: StrMap = None):
        if content is None:
            # 1. new command with text & origin info
            assert text is not None, f'receipt text should not be None, {origin}'
            cmd = ReceiptCommand.RECEIPT
            super().__init__(cmd=cmd)
            # text message
            self['text'] = text
            # original envelope of message responding to,
            # includes 'sn' and 'signature'
            if origin is not None:
                assert not (len(origin) == 0 or
                            'data' in origin or
                            'keys' in origin or
                            'meta' in origin or
                            'visa' in origin), f'impure envelope: {origin}'
                self['origin'] = origin
        else:
            # 2. command info from network
            assert text is None and origin is None, f'params error: {content}, {text}, {origin}'
            # create with command content
            super().__init__(content=content)
        # lazy load
        self.__env = None

    # -------- setters/getters

    @property  # Override
    def text(self) -> str:
        return self.get_str(key='text', default='')

    @property  # protected
    def origin(self) -> Optional[StrMap]:
        return self.get('origin')

    @property  # Override
    def original_envelope(self) -> Optional[Envelope]:
        if self.__env is None:
            # origin: { sender: "...", receiver: "...", time: 0 }
            self.__env = Envelope.parse(envelope=self.origin)
        return self.__env

    @property  # Override
    def original_sn(self) -> Optional[int]:
        origin = self.origin
        if origin is not None:
            sn = origin.get('sn')
            return Converter.get_int(value=sn)

    @property  # Override
    def original_signature(self) -> Optional[str]:
        origin = self.origin
        if origin is not None:
            signature = origin.get('signature')
            return Converter.get_str(value=signature)
