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

from typing import Optional

from dimp import StrMap
from dimp import Content, ContentFactory, ContentType
from dimp import Command, CommandFactory
from dimp import Envelope, InstantMessage, SecureMessage, ReliableMessage
from dimp import BaseContent

from dimp import ListContent, SecretContent

from .protocol import ReceiptCommand
from .protocol import MetaCommand, DocumentCommand

from .dkd import BaseMoneyContent, TransferMoneyContent
from .dkd import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent
from .dkd import BaseTextContent, WebPageContent, NameCardContent
from .dkd import CombineForwardContent
from .dkd import BaseQuoteContent

from .dkd import BaseReceiptCommand
from .dkd import BaseMetaCommand, BaseDocumentCommand
from .dkd import GroupCommand, InviteGroupCommand
from .dkd import ExpelGroupCommand, JoinGroupCommand
from .dkd import QuitGroupCommand, ResetGroupCommand

from .dkd import GeneralCommandFactory
from .dkd import HistoryCommandFactory
from .dkd import GroupCommandFactory

from .msg import MessageFactory


# noinspection PyMethodMayBeStatic
class MessageFactoryMixIn:
    """ MessageFactory Extensions """

    # protected
    def register_message_factories(self):
        """ Message factories """
        factory = MessageFactory()
        # Envelope factory
        Envelope.set_factory(factory=factory)
        # Message factories
        InstantMessage.set_factory(factory=factory)
        SecureMessage.set_factory(factory=factory)
        ReliableMessage.set_factory(factory=factory)

    # protected
    def register_content_factories(self):
        """ Core content factories """
        # Text
        self._set_content_factory(msg_type=ContentType.TEXT, content_class=BaseTextContent)

        # File
        self._set_content_factory(msg_type=ContentType.FILE, content_class=BaseFileContent)
        # Image
        self._set_content_factory(msg_type=ContentType.IMAGE, content_class=ImageFileContent)
        # Audio
        self._set_content_factory(msg_type=ContentType.AUDIO, content_class=AudioFileContent)
        # Video
        self._set_content_factory(msg_type=ContentType.VIDEO, content_class=VideoFileContent)

        # Web Page
        self._set_content_factory(msg_type=ContentType.PAGE, content_class=WebPageContent)

        # Name Card
        self._set_content_factory(msg_type=ContentType.NAME_CARD, content_class=NameCardContent)

        # Quote
        self._set_content_factory(msg_type=ContentType.QUOTE, content_class=BaseQuoteContent)

        # Money
        self._set_content_factory(msg_type=ContentType.MONEY, content_class=BaseMoneyContent)
        self._set_content_factory(msg_type=ContentType.TRANSFER, content_class=TransferMoneyContent)
        # ...

        # Command
        self._set_content_factory(msg_type=ContentType.COMMAND, factory=GeneralCommandFactory())

        # History Command
        self._set_content_factory(msg_type=ContentType.HISTORY, factory=HistoryCommandFactory())

        # Content Array
        self._set_content_factory(msg_type=ContentType.ARRAY, content_class=ListContent)

        # Combine and Forward
        self._set_content_factory(msg_type=ContentType.COMBINE_FORWARD, content_class=CombineForwardContent)

        # Top-Secret
        self._set_content_factory(msg_type=ContentType.FORWARD, content_class=SecretContent)

        # Unknown Content Type
        self._set_content_factory(msg_type=ContentType.ANY, content_class=BaseContent)

    def _set_content_factory(self, msg_type: str, content_class=None, factory: ContentFactory = None):
        if factory is not None:
            Content.set_factory(msg_type, factory=factory)
        if content_class is not None:
            factory = ContentParser(content_class=content_class)
            Content.set_factory(msg_type, factory=factory)

    # protected
    def register_command_factories(self):
        """ Core command factories """
        # Meta Command
        self._set_command_factory(cmd=MetaCommand.META, command_class=BaseMetaCommand)

        # Document Command
        self._set_command_factory(cmd=DocumentCommand.DOCUMENTS, command_class=BaseDocumentCommand)

        # Receipt Command
        self._set_command_factory(cmd=ReceiptCommand.RECEIPT, command_class=BaseReceiptCommand)

        # Group Commands
        self._set_command_factory(cmd='group', factory=GroupCommandFactory())
        self._set_command_factory(cmd=GroupCommand.INVITE, command_class=InviteGroupCommand)
        # 'expel' is deprecated (use 'reset' instead)
        self._set_command_factory(cmd=GroupCommand.EXPEL, command_class=ExpelGroupCommand)
        self._set_command_factory(cmd=GroupCommand.JOIN, command_class=JoinGroupCommand)
        self._set_command_factory(cmd=GroupCommand.QUIT, command_class=QuitGroupCommand)
        # 'query' is deprecated
        # self._set_command_factory(cmd=GroupCommand.QUERY, command_class=QueryGroupCommand)
        self._set_command_factory(cmd=GroupCommand.RESET, command_class=ResetGroupCommand)

    def _set_command_factory(self, cmd: str, command_class=None, factory: CommandFactory = None):
        if factory is not None:
            Command.set_factory(cmd=cmd, factory=factory)
        if command_class is not None:
            factory = CommandParser(command_class=command_class)
            Command.set_factory(cmd=cmd, factory=factory)


class ContentParser(ContentFactory):

    def __init__(self, content_class):
        super().__init__()
        self.__class = content_class

    # Override
    def parse_content(self, content: StrMap) -> Optional[Content]:
        # return self.__class(content=content)
        return self.__class(content)


class CommandParser(CommandFactory):

    def __init__(self, command_class):
        super().__init__()
        self.__class = command_class

    # Override
    def parse_command(self, content: StrMap) -> Optional[Command]:
        # return self.__class(content=content)
        return self.__class(content)
