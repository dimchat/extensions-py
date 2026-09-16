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

from typing import Union

from dimp import AddressExtension, IDExtension, MetaExtension, DocumentExtension
from dimp import GeneralAccountExtension, shared_account_extensions

from dimp import MessageExtensions, ContentExtension
from dimp import InstantMessageExtension, SecureMessageExtension, ReliableMessageExtension
from dimp import MessageHandlerExtension, shared_message_extensions

from dimp import CommandExtension

from .ext import AccountGeneralFactory
from .ext import MessageGeneralFactory, CommandGeneralFactory


# noinspection PyMethodMayBeStatic
class CoreMixIn:
    """ Core Extensions """

    # protected
    def register_account_helpers(self):
        # mkm
        helper = AccountGeneralFactory()
        ext = account_extensions()
        ext.address_helper = helper
        ext.id_helper = helper
        ext.meta_helper = helper
        ext.doc_helper = helper
        ext.helper = helper

    # protected
    def register_message_helpers(self):
        # dkd
        helper = MessageGeneralFactory()
        ext = message_extensions()
        ext.content_helper = helper
        ext.envelope_helper = helper
        ext.instant_helper = helper
        ext.secure_helper = helper
        ext.reliable_helper = helper
        ext.helper = helper

    # protected
    def register_command_helpers(self):
        # cmd
        helper = CommandGeneralFactory()
        ext = command_extensions()
        ext.cmd_helper = helper
        ext.command_helper = helper


def account_extensions() -> Union[AddressExtension, IDExtension, MetaExtension, DocumentExtension,
                                  GeneralAccountExtension]:
    return shared_account_extensions


def message_extensions() -> Union[MessageExtensions, ContentExtension,
                                  InstantMessageExtension, SecureMessageExtension, ReliableMessageExtension,
                                  MessageHandlerExtension]:
    return shared_message_extensions


def command_extensions() -> CommandExtension:
    return shared_message_extensions
