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

from typing import Dict, Optional

from dimp import StrMap
from dimp import ID
from dimp import EncryptedBundle
from dimp import InstantMessage, SecureMessage, SecureMessageFactory
from dimp import PlainData, TransportableData
from dimp import EncryptedMessage, NetworkMessage
from dimp import shared_message_extensions


class GeneralSecureMessageFactory(SecureMessageFactory):
    """ SecureMessage Factory """

    # Override
    def create_secure_message(self, i_msg: InstantMessage, data: bytes,
                              bundles: Optional[Dict[ID, EncryptedBundle]]):
        helper = shared_message_extensions.handler
        if helper.is_broadcast(i_msg):
            encoded_data = PlainData.create_with_bytes(data)  # UTF8.decode(data)
        else:
            encoded_data = TransportableData.create(data=data)
        assert not encoded_data.is_empty, f'failed to encode content data: {len(data)} byte(s)'
        msg_keys = None
        if bundles is not None:
            msg_keys = {}
            assert not helper.is_broadcast(i_msg), f'broadcast message should not contains keys: {i_msg}'
            for receiver, bundle in bundles.items():
                encoded_keys = bundle.encode(receiver)
                if len(encoded_keys) == 0:
                    # assert False, f'failed to encode key data: {receiver}'
                    continue
                msg_keys.update(encoded_keys)
        info = i_msg.to_map()
        info.pop('content', None)
        info['data'] = encoded_data.serialize()
        if msg_keys is not None and len(msg_keys) > 0:
            info['keys'] = msg_keys
        return EncryptedMessage(msg=info)

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
