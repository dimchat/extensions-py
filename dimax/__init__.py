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
    DIM-AX
    ~~~~~~

    Decentralized Instant Messaging Application eXtensions
"""


from .protocol import *
from .mem import *
from .mkm import *
from .dkd import *
from .msg import *
from .ext import *

from .ext_core import CoreMixIn
from .ext_entity import EntityMixIn
from .ext_msg import MessageFactoryMixIn, ContentParser, CommandParser
from .ext_loader import ExtensionLoader


name = "DIM-AX"

__author__ = 'Albert Moky'


__all__ = [

    #
    #   Content Extends
    #

    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'MoneyContent', 'TransferContent',

    'TextContent', 'PageContent', 'NameCard',
    'CombineContent',

    #
    #  Command Extends
    #

    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'ResetCommand',


    ################################
    #
    #   Implementations
    #
    ################################

    'MemoryCache',
    'ThanosCache',

    'MemoryCacheExtension',

    #
    #   Account Implementations
    #

    'BTCAddress', 'ETHAddress',
    'BaseAddressFactory',

    'GeneralIdentifierFactory',

    'BaseMeta',
    'DefaultMeta', 'BTCMeta', 'ETHMeta',
    'BaseMetaFactory',

    'BaseDocument',
    'BaseVisa', 'BaseBulletin',
    'GeneralDocumentFactory',

    #
    #   Content Implementations
    #

    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',

    'BaseMoneyContent', 'TransferMoneyContent',

    'BaseTextContent', 'WebPageContent', 'NameCardContent',
    'CombineForwardContent',

    #
    #   Command Implementations
    #

    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand', 'QuitGroupCommand', 'ResetGroupCommand',

    #
    #   Message Factories
    #

    'GeneralCommandFactory',
    'HistoryCommandFactory',
    'GroupCommandFactory',

    'MessageFactory',

    #
    #   Core Extensions
    #

    'AccountGeneralFactory',
    'MessageGeneralFactory', 'CommandGeneralFactory',

    #
    #   Loaders
    #

    'CoreMixIn',
    'EntityMixIn',
    'MessageFactoryMixIn',
    'ContentParser', 'CommandParser',
    'ExtensionLoader',

]
