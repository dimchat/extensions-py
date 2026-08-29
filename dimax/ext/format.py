# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2023 Albert Moky
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

from collections.abc import Mapping
from typing import Optional, Any

from dimp import StrMap
from dimp import URI, Mapper, Wrapper
from dimp import DecryptKey
from dimp import JSONMap
from dimp import DataURI
from dimp import TransportableData, TransportableDataFactory
from dimp import TransportableFile, TransportableFileFactory
from dimp import TransportableDataHelper
from dimp import TransportableFileHelper


class FormatGeneralFactory(TransportableDataHelper, TransportableFileHelper):

    def __init__(self):
        super().__init__()
        self.__ted_factory: Optional[TransportableDataFactory] = None
        self.__pnf_factory: Optional[TransportableFileFactory] = None

    #
    #   TED - Transportable Encoded Data
    #

    # Override
    def set_transportable_data_factory(self, factory: TransportableDataFactory):
        self.__ted_factory = factory

    # Override
    def get_transportable_data_factory(self) -> Optional[TransportableDataFactory]:
        return self.__ted_factory

    # Override
    def parse_transportable_data(self, ted: Any) -> Optional[TransportableData]:
        if ted is None:
            return None
        elif isinstance(ted, TransportableData):
            return ted
        # unwrap
        string = Wrapper.get_str(ted)
        if string is None:
            # assert False, f'TED error: {ted}'
            return None
        factory = self.get_transportable_data_factory()
        assert factory is not None, 'TED factory not set'
        return factory.parse_transportable_data(string)

    #
    #   PNF - Portable Network File
    #

    # Override
    def set_transportable_file_factory(self, factory: TransportableFileFactory):
        self.__pnf_factory = factory

    # Override
    def get_transportable_file_factory(self) -> Optional[TransportableFileFactory]:
        return self.__pnf_factory

    # Override
    def create_transportable_file(self, data: Optional[TransportableData], filename: Optional[str],
                                  url: Optional[URI], password: Optional[DecryptKey]) -> TransportableFile:
        factory = self.get_transportable_file_factory()
        assert factory is not None, 'PNF factory not ready'
        return factory.create_transportable_file(data=data, filename=filename, url=url, password=password)

    # Override
    def parse_transportable_file(self, pnf: Any) -> Optional[TransportableFile]:
        if pnf is None:
            return None
        elif isinstance(pnf, TransportableFile):
            return pnf
        # unwrap
        info = self._get_transportable_file_content(pnf)
        if info is None:
            # assert False, f'PNF error: {pnf}'
            return None
        factory = self.get_transportable_file_factory()
        assert factory is not None, 'PNF factory not ready'
        return factory.parse_transportable_file(info)

    # noinspection PyMethodMayBeStatic
    def _get_transportable_file_content(self, pnf: Any) -> Optional[StrMap]:
        if isinstance(pnf, Mapper):
            return pnf.to_map()
        elif isinstance(pnf, Mapping):
            return pnf
        text = Wrapper.get_str(pnf)
        if text is None or len(text) < 8:
            # assert False, f'PNF error: {pnf}'
            return None
        elif text.startswith('{'):
            # decode JSON string
            assert text.endswith('}'), f'PNF json error: {pnf}'
            return JSONMap.decode(string=text)
        content = {}
        # 1. check for URL: 'http://...'
        pos = text.find('://')
        if 0 < pos < 8:
            content['URL'] = text
            return content
        content['data'] = text
        # 2. check for data URI: 'data:image/jpeg;base64,...'
        uri = DataURI.parse(text)
        if uri is not None:
            extra = uri.parameters
            if extra is not None:
                filename = extra.get('filename')
                if filename is not None:
                    content['filename'] = filename
        # else:
        #     # 3. check for Base-64 encoded string?
        #     pass
        return content
