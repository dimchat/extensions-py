# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2026 Albert Moky
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
    Transportable Resource
    ~~~~~~~~~~~~~~~~~~~~~~

    TED, PNF
"""

from typing import Optional

from dimp import StrMap
from dimp import DecryptKey
from dimp import URI, DataURI
from dimp import TransportableData, TransportableDataFactory
from dimp import EmbedData, Base64Data

from .file import TransportableFile, TransportableFileFactory
from .pnf import PortableNetworkFile


class BaseNetworkDataFactory(TransportableDataFactory):

    # Override
    def parse_transportable_data(self, ted: str) -> Optional[TransportableData]:
        # check data URI
        uri = DataURI.parse(uri=ted)
        if uri is not None:
            # "data:image/jpeg;base64,..."
            return EmbedData.create_with_uri(uri=uri)
        # TODO: check Base-64 format
        # "{BASE64_ENCODED}"
        return Base64Data.create(string=ted)


class BaseNetworkFileFactory(TransportableFileFactory):

    # Override
    def create_transportable_file(self, data: Optional[TransportableData], filename: Optional[str], url: Optional[URI],
                                  password: Optional[DecryptKey]) -> TransportableFile:
        return PortableNetworkFile(None, data=data, filename=filename, url=url, password=password)

    # Override
    def parse_transportable_file(self, pnf: StrMap) -> Optional[TransportableFile]:
        # check 'data', 'URL', 'filename'
        if 'data' in pnf or 'URL' in pnf or 'filename' in pnf:
            return PortableNetworkFile(dictionary=pnf)
        # pnf.data and pnf.URL and pnf.filename should not be empty at the same time


# noinspection PyMethodMayBeStatic
class TransportableMixIn:
    """ Transportable Plugins """

    # protected
    def register_ted_factory(self):
        # TED
        factory = BaseNetworkDataFactory()
        TransportableData.set_factory(factory=factory)

    # protected
    def register_pnf_factory(self):
        # PNF
        factory = BaseNetworkFileFactory()
        PortableNetworkFile.set_factory(factory=factory)
