# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2022 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

from typing import Optional, Union

from dimp import StrMap
from dimp import Content, ContentFactory
from dimp import Command, CommandFactory
from dimp import BaseCommand
from dimp import CommandExtension, CmdExtension, shared_message_extensions

from ..protocol.groups import BaseHistoryCommand, BaseGroupCommand


"""
    General Command Factory
    ~~~~~~~~~~~~~~~~~~~~~~~
"""


class GeneralCommandFactory(ContentFactory, CommandFactory):

    # Override
    def parse_content(self, content: StrMap) -> Optional[Content]:
        # get factory by command name
        cmd = get_cmd(content=content)
        factory = None if cmd is None else get_command_factory(cmd=cmd)
        if factory is None:
            # check for group command
            if 'group' in content:  # and cmd != 'group':
                factory = get_command_factory(cmd='group')
            if factory is None:
                factory = self
        return factory.parse_command(content=content)

    # Override
    def parse_command(self, content: StrMap) -> Optional[Command]:
        # check 'sn', 'command'
        if 'sn' not in content or 'command' not in content:
            # content.sn should not be empty
            # content.command should not be empty
            return None
        # OK
        return BaseCommand(content=content)


class HistoryCommandFactory(GeneralCommandFactory):

    # Override
    def parse_command(self, content: StrMap) -> Optional[Command]:
        # check 'sn', 'command', 'time'
        if 'sn' not in content or 'command' not in content or 'time' not in content:
            # content.sn should not be empty
            # content.command should not be empty
            # content.time should not be empty
            return None
        #  OK
        return BaseHistoryCommand(content=content)


class GroupCommandFactory(HistoryCommandFactory):

    # Override
    def parse_content(self, content: StrMap) -> Optional[Content]:
        # get factory by command name
        cmd = get_cmd(content=content)
        factory = cmd if cmd is None else get_command_factory(cmd=cmd)
        if factory is None:
            factory = self
        return factory.parse_command(content=content)

    # Override
    def parse_command(self, content: StrMap) -> Optional[Command]:
        # check 'sn', 'command', 'group
        if 'sn' not in content or 'command' not in content or 'group' not in content:
            # content.sn should not be empty
            # content.command should not be empty
            # content.group should not be empty
            return None
        #  OK
        return BaseGroupCommand(content=content)


def get_cmd(content: StrMap, default: Optional[str] = None) -> Optional[str]:
    ext = command_extensions()
    helper = ext.cmd_helper
    return helper.get_cmd(content=content, default=default)


def get_command_factory(cmd: str) -> Optional[CommandFactory]:
    ext = command_extensions()
    helper = ext.command_helper
    return helper.get_command_factory(cmd=cmd)


def command_extensions() -> Union[CommandExtension, CmdExtension]:
    return shared_message_extensions
