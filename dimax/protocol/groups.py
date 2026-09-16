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
    Group Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~

    1. invite member
    2. expel member
    3. member quit
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from dimp import StrMap
from dimp import ID

from dimp import ContentType
from dimp import Command

from .base import BaseCommand


# noinspection PyAbstractClass
class HistoryCommand(Command, ABC):
    """History command interface for recording operational history.

    Base interface for all history-tracking commands, which record the timestamp
    and parameters of system operations (e.g., group member changes).

    All group-related commands implement this interface to form the group's change history.

    JSON format:
    ```json
    {
      "type" : i2s(0x89),
      "sn"   : 12345,

      "command" : "...",   // Unique history command name
      "time"    : 123.45,  // Timestamp when the command was executed

      "extra"   : info     // Optional command-specific parameters
    }
    ```
    """

    # -------- history command names begin --------
    # account
    REGISTER = "register"
    SUICIDE = "suicide"
    # -------- history command names end --------


class GroupCommand(HistoryCommand, ABC):
    """Group command interface for tracking group member/role changes.

    Extends `HistoryCommand` to define group-specific operations, which collectively
    form the complete change history of a group's member information (members, admins, owner).

    JSON format:
    ```json
    {
      "type" : i2s(0x89),
      "sn"   : 12345,

      "command" : "reset",          // "invite", "quit", "query", ...
      "time"    : 123.45,           // Timestamp of the group operation

      "group"   : "{GROUP_ID}",     // Target group ID
      "members" : ["{MEMBER_ID}",]  // List of affected member IDs
    }
    ```
    """

    # -------- group command names begin --------
    # founder/owner
    FOUND = "found"
    ABDICATE = "abdicate"
    # member
    INVITE = "invite"
    EXPEL = "expel"    # Deprecated (use 'reset' instead)
    JOIN = "join"
    QUIT = "quit"
    # QUERY = "query"  # Deprecated
    RESET = "reset"
    # administrator/assistant
    HIRE = "hire"
    FIRE = "fire"
    RESIGN = "resign"
    # -------- group command names end --------

    @property
    @abstractmethod
    def members(self) -> Optional[List[ID]]:
        """List of member IDs affected by this group command."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.members getter'
        )

    @members.setter
    @abstractmethod
    def members(self, users: Optional[List[ID]]):
        """ Set group members """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.members setter'
        )

    #
    #   Factories
    #

    @classmethod
    def create(cls, cmd: str, group: ID, members: List[ID] = None):
        return BaseGroupCommand(cmd=cmd, group=group, members=members)

    @classmethod
    def invite(cls, group: ID, members: List[ID]):
        return InviteGroupCommand(group=group, members=members)

    @classmethod
    def expel(cls, group: ID, members: List[ID]):
        """ Deprecated (use 'reset' instead) """
        return ExpelGroupCommand(group=group, members=members)

    @classmethod
    def join(cls, group: ID):
        return JoinGroupCommand(group=group)

    @classmethod
    def quit(cls, group: ID):
        return QuitGroupCommand(group=group)

    @classmethod
    def reset(cls, group: ID, members: List[ID]):
        return ResetGroupCommand(group=group, members=members)


# noinspection PyAbstractClass
class InviteCommand(GroupCommand, ABC):
    """Group invite command interface.

    Used to record the history of inviting users to join a group.
    The `members` field contains the IDs of users being invited.
    """

    @property
    @abstractmethod
    def welcome(self) -> str:
        """ The welcome/joining text sent with the invitation. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.welcome getter'
        )


# noinspection PyAbstractClass
class ExpelCommand(GroupCommand, ABC):
    """Group expel command interface (DEPRECATED).

    Originally used to record the history of expelling members from a group.
    This command is deprecated - use `ResetCommand` (RESET) instead for member removal.
    """

    @property
    @abstractmethod
    def away(self) -> str:
        """ The farewell/leaving text sent with the expulsion. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.away getter'
        )


# noinspection PyAbstractClass
class JoinCommand(GroupCommand, ABC):
    """Group join command interface.

    Used to record the history of users voluntarily joining a group.
    The `members` field contains the ID of the user joining the group.
    """

    @property
    @abstractmethod
    def ask(self) -> str:
        """ The question/application text of the user requesting to join. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.ask getter'
        )


# noinspection PyAbstractClass
class QuitCommand(GroupCommand, ABC):
    """Group quit command interface.

    Used to record the history of members voluntarily leaving a group.
    The `members` field contains the ID of the member quitting the group.
    """

    @property
    @abstractmethod
    def bye(self) -> str:
        """ The farewell/leaving text of the member quitting the group. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.bye getter'
        )


# noinspection PyAbstractClass
class ResetCommand(GroupCommand, ABC):
    """Group reset command interface.

    Used to record the history of resetting the full list of group members,
    replacing deprecated commands like EXPEL and QUERY. This command is the
    standard way to update the complete member list (add/remove multiple members).

    JSON format:
    ```json
    {
      "type" : i2s(0x89),
      "sn"   : 12345,

      "command" : "reset",
      "time"    : 123.45,        // Timestamp of the reset operation

      "group"   : "{GROUP_ID}",  // Target group ID
      "members" : [...]          // Full list of current group members after reset
    }
    ```
    """

    @property
    @abstractmethod
    def confirm(self) -> str:
        """ The confirmation text sent with the reset command. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.confirm getter'
        )


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseHistoryCommand(BaseCommand, HistoryCommand):

    def __init__(self, content: StrMap = None,
                 msg_type: str = None, cmd: str = None):
        if content is None:
            if msg_type is None:
                msg_type = ContentType.HISTORY
            assert cmd is not None, 'command name should not empty'
        super().__init__(content, msg_type, cmd=cmd)


class BaseGroupCommand(BaseHistoryCommand, GroupCommand):

    def __init__(self, content: StrMap = None,
                 cmd: str = None, group: ID = None, members: List[ID] = None):
        super().__init__(content, None, cmd=cmd)
        if group is not None:
            self.group = group
        if members is not None:
            self.members = members

    @property  # Override
    def members(self) -> Optional[List[ID]]:
        array = self.get('members')
        if array is not None:
            # convert all items to ID objects
            return ID.convert(array=array)
        # get from 'member'
        single = ID.parse(identifier=self.get('member'))
        if single is not None:
            return [single]
        # assert False, 'failed to get group members'

    @members.setter  # Override
    def members(self, users: List[ID]):
        if users is None:
            self.pop('members', None)
        else:
            self['members'] = ID.revert(identifiers=users)
        self.pop('member', None)


class InviteGroupCommand(BaseGroupCommand, InviteCommand):

    def __init__(self, content: StrMap = None,
                 group: ID = None, members: List[ID] = None):
        cmd = GroupCommand.INVITE if content is None else None
        super().__init__(content, cmd=cmd, group=group, members=members)

    @property  # Override
    def welcome(self) -> str:
        return self.get_str(key='text', default='')


class ExpelGroupCommand(BaseGroupCommand, ExpelCommand):
    """ Deprecated, use 'reset' instead """

    def __init__(self, content: StrMap = None,
                 group: ID = None, members: List[ID] = None):
        cmd = GroupCommand.EXPEL if content is None else None
        super().__init__(content, cmd=cmd, group=group, members=members)

    @property  # Override
    def away(self) -> str:
        return self.get_str(key='text', default='')


class JoinGroupCommand(BaseGroupCommand, JoinCommand):

    def __init__(self, content: StrMap = None, group: ID = None):
        cmd = GroupCommand.JOIN if content is None else None
        super().__init__(content, cmd=cmd, group=group)

    @property  # Override
    def ask(self) -> str:
        return self.get_str(key='text', default='')


class QuitGroupCommand(BaseGroupCommand, QuitCommand):

    def __init__(self, content: StrMap = None, group: ID = None):
        cmd = GroupCommand.QUIT if content is None else None
        super().__init__(content, cmd=cmd, group=group)

    @property  # Override
    def bye(self) -> str:
        return self.get_str(key='text', default='')


class ResetGroupCommand(BaseGroupCommand, ResetCommand):

    def __init__(self, content: StrMap = None, group: ID = None, members: List[ID] = None):
        cmd = GroupCommand.RESET if content is None else None
        super().__init__(content, cmd=cmd, group=group, members=members)

    @property  # Override
    def confirm(self) -> str:
        return self.get_str(key='text', default='')
