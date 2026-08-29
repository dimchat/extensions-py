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

import random
import threading
from typing import Optional

from dimp import StrMap
from dimp import DateTime
from dimp import ID
from dimp import Content, Envelope
from dimp import InstantMessage, SecureMessage, ReliableMessage
from dimp import EnvelopeFactory, InstantMessageFactory, SecureMessageFactory, ReliableMessageFactory
from dimp import MessageEnvelope, PlainMessage, EncryptedMessage, NetworkMessage


class MessageFactory(EnvelopeFactory, InstantMessageFactory, SecureMessageFactory, ReliableMessageFactory):

    def __init__(self):
        super().__init__()
        self.__sn = random.randint(0, 0x7fffffff)  # 0 ~ 0x7fffffff
        self.__lock = threading.Lock()

    def __next(self) -> int:
        """ return 1 ~ 2^31-1 """
        sn = self.__sn
        assert sn >= 0, f'serial number error: {sn}'
        with self.__lock:
            sn = self.__sn
            if sn < 0x7fffffff:  # 2 ** 31 - 1
                sn += 1
            else:
                sn = 1
            self.__sn = sn
            return sn

    #
    #   EnvelopeFactory
    #

    # Override
    def create_envelope(self, sender: ID, receiver: ID, time: Optional[DateTime]) -> Envelope:
        return MessageEnvelope(sender=sender, receiver=receiver, time=time)

    # Override
    def parse_envelope(self, envelope: StrMap) -> Optional[Envelope]:
        # check 'sender'
        if 'sender' not in envelope:
            # env.sender should not empty
            return None
        # OK
        return MessageEnvelope(envelope=envelope)

    #
    #   InstantMessageFactory
    #

    # Override
    def generate_serial_number(self, msg_type: Optional[str], now: Optional[DateTime]) -> int:
        # because we must make sure all messages in a same chat box won't have
        # same serial numbers, so we can't use time-related numbers, therefore
        # the best choice is a totally random number, maybe.
        return self.__next()

    # Override
    def create_instant_message(self, head: Envelope, body: Content) -> InstantMessage:
        return PlainMessage(head=head, body=body)

    # Override
    def parse_instant_message(self, msg: StrMap) -> Optional[InstantMessage]:
        # check 'sender', 'content'
        if 'sender' not in msg or 'content' not in msg:
            # msg.sender should not be empty
            # msg.content should not be empty
            return None
        # OK
        return PlainMessage(msg=msg)

    #
    #   SecureMessageFactory
    #

    # Override
    def parse_secure_message(self, msg: StrMap) -> Optional[SecureMessage]:
        # check 'sender', 'data'
        if 'sender' not in msg or 'data' not in msg:
            # msg.sender should not be empty
            # msg.data should not be empty
            return None
        # check 'signature'
        if 'signature' in msg:
            return NetworkMessage(msg=msg)
        # OK
        return EncryptedMessage(msg=msg)

    #
    #   ReliableMessageFactory
    #

    # Override
    def parse_reliable_message(self, msg: StrMap) -> Optional[ReliableMessage]:
        # check 'sender', 'data', 'signature'
        if 'sender' not in msg or 'data' not in msg or 'signature' not in msg:
            # msg.sender should not be empty
            # msg.data should not be empty
            # msg.signature should not be empty
            return None
        # OK
        return NetworkMessage(msg=msg)
