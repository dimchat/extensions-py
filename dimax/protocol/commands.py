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

from abc import ABC, abstractmethod
from typing import Optional, List

from dimp import StrMap
from dimp import DateTime

from dimp import ID
from dimp import Meta, Document

from dimp import Command

from .base import BaseCommand


#############################
#                           #
#       Core Commands       #
#                           #
#############################


class MetaCommand(Command, ABC):
    """Meta command interface for querying/updating entity metadata.

    Used to request or respond with an entity's core metadata (e.g. user/group info).

    JSON format:
    ```json
    {
      "type" : i2s(0x88),
      "sn"   : 12345,

      "command" : "meta",  // Fixed command name
      "did"     : "{ID}",  // Target entity ID (user/group ID)
      "meta"    : {...}    // Entity metadata (null = query request)
    }
    ```
    """

    META = 'meta'  # querying/updating entity metadata

    #
    #   ID
    #
    @property
    @abstractmethod
    def identifier(self) -> ID:
        """Gets the target entity ID (user/group ID) for this meta command.

        This ID identifies the entity whose metadata is being queried or updated.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.identifier getter'
        )

    #
    #   Meta
    #
    @property
    @abstractmethod
    def meta(self) -> Optional[Meta]:
        """Gets the entity metadata associated with this command.

        - Non-null: Response with metadata for the target `identifier`
        - Null: Query request for metadata of the target `identifier`
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.meta getter'
        )

    #
    #   Factories
    #

    @classmethod
    def query(cls, identifier: ID):  # -> MetaCommand:
        """Creates a query meta command to request entity metadata.

        Use this to ask for metadata of a specific entity (meta field will be null).

        `identifier` is the target entity ID (user/group ID) to query.

        Returns a `MetaCommand` instance for metadata query.

        :param identifier: entity ID
        :return: MetaCommand
        """
        return BaseMetaCommand(identifier=identifier)

    @classmethod
    def response(cls, identifier: ID, meta: Meta):  # -> MetaCommand:
        """Creates a response meta command with entity metadata.

        Use this to send metadata back to a query request.

        `identifier` is the target entity ID (user/group ID).
        `meta` is the metadata to return for the entity.

        Returns a `MetaCommand` instance containing the metadata.

        :param identifier: entity ID
        :param meta: entity meta
        :return: MetaCommand
        """
        return BaseMetaCommand(identifier=identifier, meta=meta)


class DocumentCommand(MetaCommand, ABC):
    """Document command interface for querying/updating entity documents.

    Extends `MetaCommand` to support document operations (Visa for users, Bulletin for groups).
    Used to exchange entity documents or request updates.

    JSON format:
    ```json
    {
      "type" : i2s(0x88),
      "sn"   : 12345,

      "command"   : "documents",  // Fixed command name
      "did"       : "{ID}",       // Target entity ID (user/group ID)
      "meta"      : {...},        // Optional metadata (for new friend handshakes)
      "documents" : [...],        // Entity documents (null = query request)
      "last_time" : 123.45        // Optional: Timestamp for incremental updates
    }
    ```
    """

    DOCUMENTS = 'documents'  # querying/updating entity documents

    #
    #   documents
    #
    @property
    @abstractmethod
    def documents(self) -> Optional[List[Document]]:
        """Gets the list of entity documents (Visa/Bulletin) for this command.

        - Non-null: Response with documents for the target `identifier`
        - Null: Query request for documents of the target `identifier`
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.documents getter'
        )

    @property
    @abstractmethod
    def last_time(self) -> Optional[DateTime]:
        """Gets the timestamp for incremental document queries.

        Used to request only documents updated after this time (for efficient sync).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.last_time getter'
        )

    #
    #   Factories
    #

    @classmethod
    def query(cls, identifier: ID, last_time: DateTime = None):  # -> DocumentCommand:
        """Creates a query document command to request entity documents.

        Use this to:
        1. Query all documents for an entity (omit `last_time`)
        2. Query incremental updates (provide `last_time` for updates since then)

        `identifier` is the target entity ID (user/group ID) to query.
        `last_time` is the optional timestamp for incremental updates.

        Returns a `DocumentCommand` instance for document query.

        :param identifier: entity ID
        :param last_time:  last document time
        :return: DocumentCommand
        """
        return BaseDocumentCommand(identifier=identifier, last_time=last_time)

    @classmethod
    def response(cls, documents: List[Document], meta: Optional[Meta] = None, identifier: ID = None):
        """Creates a response document command with entity documents.

        Use this to:
        1. Send metadata + documents to a new friend (handshake)
        2. Respond to a document query request

        `identifier` is the target entity ID (user/group ID).
        `meta` is the optional metadata (for handshake scenarios).
        `documents` is the list of documents to return for the entity.

        Returns a `DocumentCommand` instance containing the documents.

        :param identifier: entity ID
        :param meta:       entity meta
        :param documents:  entity documents
        :return: DocumentCommand
        """
        return BaseDocumentCommand(identifier=identifier, meta=meta, documents=documents)


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseMetaCommand(BaseCommand, MetaCommand):

    def __init__(self, content: StrMap = None,
                 cmd: str = None,
                 identifier: ID = None,
                 meta: Optional[Meta] = None):
        if content is None:
            # 1. new command with name, ID & meta
            assert identifier is not None, f'meta command error: {cmd}, {identifier}, {meta}'
            if cmd is None:
                cmd = MetaCommand.META
            super().__init__(cmd=cmd)
            self.set_string(key='did', value=identifier)
            if meta is not None:
                self.set_map(key='meta', value=meta)
        else:
            # 2. command info from network
            assert cmd is None and identifier is None and meta is None, \
                f'params error: {content}, {cmd}, {identifier}, {meta}'
            super().__init__(content)
        # lazy load
        self.__meta = meta

    #
    #   ID
    #
    @property  # Override
    def identifier(self) -> ID:
        return ID.parse(identifier=self.get('did'))

    #
    #   Meta
    #
    @property  # Override
    def meta(self) -> Optional[Meta]:
        if self.__meta is None:
            self.__meta = Meta.parse(meta=self.get('meta'))
        return self.__meta


class BaseDocumentCommand(BaseMetaCommand, DocumentCommand):

    def __init__(self, content: StrMap = None,
                 identifier: ID = None,
                 meta: Optional[Meta] = None,
                 documents: List[Document] = None,
                 last_time: Optional[DateTime] = None):
        if content is None:
            # 1. new command with ID, meta, document & signature
            assert identifier is not None, f'document command error: {meta}, {documents}, {last_time}'
            cmd = DocumentCommand.DOCUMENTS
            super().__init__(cmd=cmd, identifier=identifier, meta=meta)
            # respond with document info
            if documents is not None:
                self['documents'] = Document.revert(documents=documents)
            # query with last document time
            if last_time is not None:
                self.set_datetime(key='last_time', value=last_time)
        else:
            # 2. command info from network
            assert identifier is None and meta is None and documents is None and last_time is None, \
                f'params error: {content}, {identifier}, {meta}, {documents}, {last_time}'
            super().__init__(content)
        # lazy load
        self.__docs = documents

    #
    #   document
    #
    @property  # Override
    def documents(self) -> Optional[List[Document]]:
        if self.__docs is None:
            docs = self.get('documents')
            if docs is not None:
                self.__docs = Document.convert(array=docs)
        return self.__docs

    @property  # Override
    def last_time(self) -> Optional[DateTime]:
        return self.get_datetime(key='last_time')
