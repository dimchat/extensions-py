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
    DIM-AX - Message Contents & Commands
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Application extends for DIM protocol
"""

from .assets import MoneyContent, TransferContent
# from .assets import BaseMoneyContent, TransferMoneyContent

from .files import FileContent, ImageContent, AudioContent, VideoContent
# from .files import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent

from .contents import TextContent
from .contents import PageContent, NameCard
# from .contents import BaseTextContent, WebPageContent, NameCardContent

from .combine import CombineContent
# from .combine import CombineForwardContent

from .quote import QuoteContent
# from .quote import BaseQuoteContent

from .receipt import ReceiptCommand
# from .receipt import BaseReceiptCommand

from .commands import MetaCommand, DocumentCommand
# from .commands import BaseMetaCommand, BaseDocumentCommand

from .groups import HistoryCommand, GroupCommand
from .groups import InviteCommand, ExpelCommand, JoinCommand, QuitCommand, ResetCommand
# from .groups import BaseHistoryCommand, BaseGroupCommand
# from .groups import InviteGroupCommand, ExpelGroupCommand, JoinGroupCommand, QuitGroupCommand, ResetGroupCommand


__all__ = [

    #
    #  Content Extends
    #

    'MoneyContent', 'TransferContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'TextContent', 'PageContent', 'NameCard',
    'CombineContent',
    'QuoteContent',

    #
    #  Command Extends
    #

    'ReceiptCommand',
    'MetaCommand', 'DocumentCommand',
    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'ResetCommand',


    ################################
    #
    #   Implementations
    #
    ################################

    # 'BaseMoneyContent', 'TransferMoneyContent',
    # 'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    # 'BaseTextContent', 'WebPageContent', 'NameCardContent',
    # 'CombineForwardContent',
    # 'BaseQuoteContent',

    # 'BaseReceiptCommand',
    # 'BaseMetaCommand', 'BaseDocumentCommand',
    # 'BaseHistoryCommand', 'BaseGroupCommand',
    # 'InviteGroupCommand', 'ExpelGroupCommand',
    # 'JoinGroupCommand', 'QuitGroupCommand', 'ResetGroupCommand',

]
