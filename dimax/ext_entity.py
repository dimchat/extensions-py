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

from dimp import Address, ID
from dimp import MetaType, Meta, MetaFactory
from dimp import DocumentType, Document, DocumentFactory

from .mkm import GeneralIdentifierFactory
from .mkm import BaseAddressFactory
from .mkm import BaseMetaFactory
from .mkm import GeneralDocumentFactory


# noinspection PyMethodMayBeStatic
class EntityMixIn:
    """ Entity Extensions """

    # protected
    def register_id_factory(self):
        ID.set_factory(factory=GeneralIdentifierFactory())

    # protected
    def register_address_factory(self):
        Address.set_factory(factory=BaseAddressFactory())

    # protected
    def register_meta_factories(self):
        self._set_meta_factory(version=MetaType.MKM)
        self._set_meta_factory(version=MetaType.BTC)
        self._set_meta_factory(version=MetaType.ETH)

    def _set_meta_factory(self, version: str, factory: MetaFactory = None):
        if factory is None:
            factory = BaseMetaFactory(version=version)
        Meta.set_factory(version=version, factory=factory)

    # protected
    def register_document_factories(self):
        self._set_document_factory(doc_type='*')
        self._set_document_factory(doc_type=DocumentType.VISA)
        self._set_document_factory(doc_type=DocumentType.PROFILE)
        self._set_document_factory(doc_type=DocumentType.BULLETIN)

    def _set_document_factory(self, doc_type: str, factory: DocumentFactory = None):
        if factory is None:
            factory = GeneralDocumentFactory(doc_type=doc_type)
        Document.set_factory(doc_type=doc_type, factory=factory)
