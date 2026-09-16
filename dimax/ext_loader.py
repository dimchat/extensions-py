# -*- coding: utf-8 -*-
#
#   DIM-AX : Decentralized Instant Messaging Application eXtensions
#
#                                Written in 2025 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2025 Albert Moky
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

from .ext_core import CoreMixIn
from .ext_entity import EntityMixIn
from .ext_msg import MessageFactoryMixIn


# noinspection PyMethodMayBeStatic
class ExtensionLoader(CoreMixIn, EntityMixIn, MessageFactoryMixIn):
    """Core extensions loader.

    Mixes in `CoreMixIn`, `EntityMixIn` and `MessageFactoryMixIn` to
    initialize the whole SDK, registering default helpers and factories.
    """

    def load(self):
        """Register core factories.

        This is the single entry to initialize the extension SDK:
        loads core helpers, entity factories and message factories.
        """
        self._load_core_extensions()

        self._load_entity_extensions()

        self._load_message_extensions()

    def _load_core_extensions(self):
        """Register core helpers (account/message/command)."""
        self.register_account_helpers()

        self.register_message_helpers()
        self.register_command_helpers()

    def _load_entity_extensions(self):
        """Register entity factories (ID/Address/Meta/Document)."""
        self.register_id_factory()
        self.register_address_factory()

        self.register_meta_factories()

        self.register_document_factories()

    def _load_message_extensions(self):
        """Register message/command factories."""
        self.register_message_factories()

        self.register_content_factories()
        self.register_command_factories()
