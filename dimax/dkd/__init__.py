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

from ..protocol import *

from ..protocol.files import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent
from ..protocol.assets import BaseMoneyContent, TransferMoneyContent

from ..protocol.contents import BaseTextContent, WebPageContent, NameCardContent
from ..protocol.combine import CombineForwardContent
from ..protocol.quote import BaseQuoteContent

from ..protocol.receipt import BaseReceiptCommand
from ..protocol.groups import BaseHistoryCommand, BaseGroupCommand
from ..protocol.groups import InviteGroupCommand, ExpelGroupCommand
from ..protocol.groups import JoinGroupCommand, QuitGroupCommand, ResetGroupCommand

from .cmd_fact import GeneralCommandFactory
from .cmd_fact import HistoryCommandFactory
from .cmd_fact import GroupCommandFactory


__all__ = [

    #
    #   Protocol
    #

    'MoneyContent', 'TransferContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'TextContent', 'PageContent', 'NameCard',
    'CombineContent',
    'QuoteContent',

    'ReceiptCommand',
    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'ResetCommand',

    #
    #   Implementations
    #

    'BaseMoneyContent', 'TransferMoneyContent',
    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    'BaseTextContent', 'WebPageContent', 'NameCardContent',
    'CombineForwardContent',
    'BaseQuoteContent',

    'BaseReceiptCommand',
    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand',
    'JoinGroupCommand', 'QuitGroupCommand', 'ResetGroupCommand',

    #
    #   Command Factories
    #

    'GeneralCommandFactory',
    'HistoryCommandFactory',
    'GroupCommandFactory',

]
