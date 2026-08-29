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

from typing import Optional

from dimp import StrMap
from dimp import TransportableData
from dimp import DocumentType
from dimp import Document, DocumentFactory

from ..mem.ext import account_helper

from .document import BaseDocument
from .docs import BaseVisa, BaseBulletin


class GeneralDocumentFactory(DocumentFactory):
    """ General Document Factory """

    def __init__(self, doc_type: str):
        super().__init__()
        self.__type = doc_type

    @property  # protected
    def type(self) -> str:
        return self.__type

    # Override
    def create_document(self, data: Optional[str], signature: Optional[TransportableData]) -> Document:
        if data is None or len(data) == 0:
            assert signature is None, f'document error: {data}, signature: {signature}'
            # 1. create empty document
            return self._create_empty_document()
        elif signature is None or signature.is_empty:
            # assert False, f'document error: {data}, signature: {signature}'
            return self._create_empty_document()
        # 2. create document with data & signature from local storage
        return self._create_valid_document(data=data, signature=signature)

    def _create_empty_document(self) -> Document:
        """ create a new empty document """
        doc_type = self.type
        if doc_type == DocumentType.VISA:
            return BaseVisa()
        elif doc_type == DocumentType.BULLETIN:
            return BaseBulletin()
        else:
            return BaseDocument(doc_type=doc_type)

    def _create_valid_document(self, data: str, signature: TransportableData) -> Document:
        """ create document with data & signature from local storage """
        doc_type = self.type
        if doc_type == DocumentType.VISA:
            return BaseVisa(data=data, signature=signature)
        elif doc_type == DocumentType.BULLETIN:
            return BaseBulletin(data=data, signature=signature)
        else:
            return BaseDocument(doc_type=doc_type, data=data, signature=signature)

    # Override
    def parse_document(self, document: StrMap) -> Optional[Document]:
        # check 'did', 'data', 'signature'
        if 'data' not in document or 'signature' not in document:
            # document.data should not be empty
            # document.signature should not be empty
            return None
        # elif 'did' not in document:
        #     # document.did should not be empty
        #     return None
        helper = account_helper()
        # create document for type
        doc_type = helper.get_document_type(document=document)
        if doc_type == DocumentType.VISA:
            return BaseVisa(document=document)
        elif doc_type == DocumentType.BULLETIN:
            return BaseBulletin(document=document)
        else:
            return BaseDocument(document=document)
