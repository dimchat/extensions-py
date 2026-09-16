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

from dimp import StrMap
from dimp import SecureMessage, ReliableMessage, ReliableMessageFactory
from dimp import TransportableData
from dimp import NetworkMessage


class GeneralReliableMessageFactory(ReliableMessageFactory):
    """ ReliableMessage Factory """

    # Override
    def create_reliable_message(self, s_msg: SecureMessage, signature: bytes):
        #
        #  1. encode signature
        #
        base64 = TransportableData.create(data=signature)
        assert not base64.is_empty, f'failed to encode signature: {len(signature)} byte(s)' \
                                    f' {s_msg.sender} => {s_msg.receiver}, {s_msg.group}'
        #
        #  2. create message
        #
        info = s_msg.to_map()
        info['signature'] = base64.serialize()
        return NetworkMessage(msg=info)

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
