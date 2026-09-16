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
from typing import Optional

from dimp import URI
from dimp import StrMap, MutableStrMap
from dimp import TransportableData
from dimp import TransportableFile
from dimp import TransportableFileWrapper
from dimp import DecryptKey

from dimp import ContentType
from dimp import Content

from .base import BaseContent


class FileContent(Content, ABC):
    """File message content interface.

    Defines the base structure for all file-type messages (image, audio, video, etc.).
    Files can be embedded as base64 data or downloaded via CDN URL (with encryption).

    JSON format:
    ```json
    {
      "type" : i2s(0x10),
      "sn"   : 12345,

      "data"     : "...",         // Base64 encoded file content
      "filename" : "photo.png",

      "URL"      : "http://...",  // CDN download URL (file is encrypted before upload)
      "key"      : {              // Symmetric key to decrypt CDN-downloaded file
        "algorithm" : "AES",      // Encryption algorithm (e.g. AES, DES)
        "data"      : "{BASE64_ENCODE}"
      }
    }
    ```
    """

    @property
    @abstractmethod
    def data(self) -> Optional[TransportableData]:
        """Embedded file content (Base64 encoded).

        Null if file is only available via CDN URL.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.data getter'
        )

    @data.setter
    @abstractmethod
    def data(self, attachment: Optional[TransportableData]):
        """ Set file data """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.data setter'
        )

    @property
    @abstractmethod
    def filename(self) -> Optional[str]:
        """Original filename of the file (including extension).

        e.g. "photo.png", "document.pdf"
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.filename getter'
        )

    @filename.setter
    @abstractmethod
    def filename(self, name: str):
        """ Set filename """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.filename setter'
        )

    @property
    @abstractmethod
    def url(self) -> Optional[URI]:
        """CDN URL for downloading the encrypted file content.

        File content on CDN is encrypted with a symmetric key (`password`).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.url getter'
        )

    @url.setter
    @abstractmethod
    def url(self, remote: URI):
        """ Set URL """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.url setter'
        )

    @property
    @abstractmethod
    def password(self) -> Optional[DecryptKey]:
        """Symmetric decryption key for CDN-downloaded file content.

        Required to decrypt files downloaded from `url` (file is encrypted before upload to CDN).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.password getter'
        )

    @password.setter
    @abstractmethod
    def password(self, key: DecryptKey):
        """ Set symmetric key """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.password setter'
        )

    # #
    # #   PNF transforming
    # #
    #
    # @property
    # @abstractmethod
    # def transportable_file(self) -> TransportableFile:
    #     """ Convert to PNF """
    #     raise NotImplementedError(
    #         f'Not implemented: {type(self).__module__}.{type(self).__name__}.transportable_file getter'
    #     )

    #
    #  Factories
    #

    @classmethod
    def create(cls, msg_type: str,
               data: Optional[TransportableData] = None, filename: Optional[str] = None,
               url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        if msg_type == ContentType.IMAGE:
            return ImageFileContent(data=data, filename=filename, url=url, password=password)
        elif msg_type == ContentType.AUDIO:
            return AudioFileContent(data=data, filename=filename, url=url, password=password)
        elif msg_type == ContentType.VIDEO:
            return VideoFileContent(data=data, filename=filename, url=url, password=password)
        else:
            return BaseFileContent(msg_type=msg_type, data=data, filename=filename, url=url, password=password)

    @classmethod
    def file(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
             url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        return BaseFileContent(data=data, filename=filename, url=url, password=password)

    @classmethod
    def image(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
              url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        return ImageFileContent(data=data, filename=filename, url=url, password=password)

    @classmethod
    def audio(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
              url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        return AudioFileContent(data=data, filename=filename, url=url, password=password)

    @classmethod
    def video(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
              url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        return VideoFileContent(data=data, filename=filename, url=url, password=password)


class ImageContent(FileContent, ABC):
    """Image message content interface.

    Extends `FileContent` with thumbnail support for previewing images.

    JSON format:
    ```json
    {
      "type" : i2s(0x12),
      "sn"   : 12345,

      "data"     : "...",         // Base64 encoded image content
      "filename" : "photo.png",

      "URL"      : "http://...",  // CDN download URL (encrypted)
      "key"      : {              // Symmetric key to decrypt image
        "algorithm" : "AES",
        "data"      : "{BASE64_ENCODE}"
      },
      "thumbnail": "data:image/jpeg;base64,..."
    }
    ```
    """

    @property
    @abstractmethod
    def thumbnail(self) -> Optional[TransportableFile]:
        """Thumbnail preview of the image (Base64 encoded).

        Used for quick preview without downloading the full image file.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.thumbnail getter'
        )

    @thumbnail.setter
    @abstractmethod
    def thumbnail(self, img: TransportableFile):
        """ Set thumbnail of image """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.thumbnail setter'
        )


class AudioContent(FileContent, ABC):
    """Audio message content interface.

    Extends `FileContent` with speech-to-text (ASR) support for audio messages.

    JSON format:
    ```json
    {
      "type" : i2s(0x14),
      "sn"   : 12345,

      "data"     : "...",         // Base64 encoded audio content
      "filename" : "voice.mp4",

      "URL"      : "http://...",  // CDN download URL (encrypted)
      "key"      : {              // Symmetric key to decrypt audio
        "algorithm" : "AES",
        "data"      : "{BASE64_ENCODE}"
      },
      "text": "..."               // Automatic Speech Recognition (ASR) result
    }
    ```
    """

    @property
    @abstractmethod
    def duration(self) -> float:
        """Duration of the audio in seconds.

        Returns the playing duration (null if unknown).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.duration getter'
        )

    @duration.setter
    @abstractmethod
    def duration(self, value: float):
        """ Set audio duration """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.duration setter'
        )

    @property
    @abstractmethod
    def text(self) -> Optional[str]:
        """Automatic Speech Recognition (ASR) text of the audio.

        Transcribed text from the audio content (null if not transcribed).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.text getter'
        )

    @text.setter
    @abstractmethod
    def text(self, asr: str):
        """ Set text (Automatic Speech Recognition) """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.text setter'
        )


class VideoContent(FileContent, ABC):
    """Video message content interface.

    Extends `FileContent` with snapshot support for previewing videos.

    JSON format:
    ```json
    {
      "type" : i2s(0x16),
      "sn"   : 12345,

      "data"     : "...",         // Base64 encoded video content
      "filename" : "movie.mp4",

      "URL"      : "http://...",  // CDN download URL (encrypted)
      "key"      : {              // Symmetric key to decrypt video
        "algorithm" : "AES",
        "data"      : "{BASE64_ENCODE}"
      },
      "snapshot": "data:image/jpeg;base64,..."
    }
    ```
    """

    @property
    @abstractmethod
    def snapshot(self) -> Optional[TransportableFile]:
        """Snapshot (preview image) of the video (Base64 encoded).

        Usually the first frame of the video for quick preview.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.snapshot getter'
        )

    @snapshot.setter
    @abstractmethod
    def snapshot(self, img: TransportableFile):
        """ Set snapshot of video """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.snapshot setter'
        )


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseFileContent(BaseContent, FileContent):
    """ File Message Content """

    def __init__(self, content: StrMap = None,
                 msg_type: str = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        if content is None:
            # 1. new content with type, data, filename, url & password
            if msg_type is None:
                msg_type = ContentType.FILE
            super().__init__(None, msg_type)
            content = super().to_map()
        else:
            # 2. content from network
            assert msg_type is None and data is None and filename is None and url is None and password is None, \
                f'params error: {content}, {msg_type}, {data}, {filename}, {url}, {password}'
            super().__init__(content)
        # access via the wrapper
        wrapper = TransportableFileWrapper.create(content, data=data, filename=filename, url=url, password=password)
        self.__wrapper = wrapper

    # Override
    def to_map(self) -> MutableStrMap:
        """ call wrapper to serialize 'data' & 'key" """
        wrapper = self.__wrapper
        return wrapper.to_map()

    # @property  # Override
    # def transportable_file(self) -> TransportableFile:
    #     """ clone without serializations """
    #     info = super().to_map()
    #     wrapper = self.__wrapper
    #     return PortableNetworkFile(dictionary=info, wrapper=wrapper)

    @property  # Override
    def data(self) -> Optional[TransportableData]:
        wrapper = self.__wrapper
        return wrapper.data

    @data.setter  # Override
    def data(self, attachment: TransportableData):
        wrapper = self.__wrapper
        wrapper.data = attachment

    @property  # Override
    def filename(self) -> Optional[str]:
        wrapper = self.__wrapper
        return wrapper.filename

    @filename.setter  # Override
    def filename(self, name: str):
        wrapper = self.__wrapper
        wrapper.filename = name

    @property  # Override
    def url(self) -> Optional[URI]:
        wrapper = self.__wrapper
        return wrapper.url

    @url.setter  # Override
    def url(self, remote: str):
        wrapper = self.__wrapper
        wrapper.url = remote

    @property  # Override
    def password(self) -> Optional[DecryptKey]:
        wrapper = self.__wrapper
        return wrapper.password

    @password.setter  # Override
    def password(self, key: DecryptKey):
        wrapper = self.__wrapper
        wrapper.password = key


class ImageFileContent(BaseFileContent, ImageContent):
    """ Image Message Content """

    def __init__(self, content: StrMap = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.IMAGE if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)
        # small image
        self.__thumbnail: Optional[TransportableFile] = None

    # Override
    def to_map(self) -> MutableStrMap:
        # serialize 'thumbnail'
        img = self.__thumbnail
        if img is not None and self.get('thumbnail') is None:
            self['thumbnail'] = img.serialize()
        # OK
        return super().to_map()

    # @property  # Override
    # def transportable_file(self) -> TransportableFile:
    #     # serialize 'thumbnail'
    #     img = self.__thumbnail
    #     if img is not None and self.get('thumbnail') is None:
    #         self['thumbnail'] = img.serialize()
    #     # clone without other serializations
    #     return super().transportable_file

    @property  # Override
    def thumbnail(self) -> Optional[TransportableFile]:
        img = self.__thumbnail
        if img is None:
            base64 = self.get('thumbnail')
            img = TransportableFile.parse(base64)
            self.__thumbnail = img
        return img

    @thumbnail.setter  # Override
    def thumbnail(self, img: TransportableFile):
        self.pop('thumbnail', None)
        # self['thumbnail'] = None if img is None else img.serialize()
        self.__thumbnail = img


class AudioFileContent(BaseFileContent, AudioContent):
    """ Audio Message Content """

    def __init__(self, content: StrMap = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.AUDIO if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)

    @property  # Override
    def duration(self) -> float:
        return self.get_float(key='duration', default=0)

    @duration.setter  # Override
    def duration(self, value: float):
        self['duration'] = value

    @property  # Override
    def text(self) -> Optional[str]:
        return self.get_str(key='text')

    @text.setter  # Override
    def text(self, asr: str):
        self['text'] = asr


class VideoFileContent(BaseFileContent, VideoContent):
    """ Video Message Content """

    def __init__(self, content: StrMap = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.VIDEO if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)
        # small image
        self.__snapshot: Optional[TransportableFile] = None

    # Override
    def to_map(self) -> MutableStrMap:
        # serialize 'snapshot'
        img = self.__snapshot
        if img is not None and self.get('snapshot') is None:
            self['snapshot'] = img.serialize()
        # OK
        return super().to_map()

    # @property  # Override
    # def transportable_file(self) -> TransportableFile:
    #     # serialize 'snapshot'
    #     img = self.__snapshot
    #     if img is not None and self.get('snapshot') is None:
    #         self['snapshot'] = img.serialize()
    #     # clone without other serializations
    #     return super().transportable_file

    @property  # Override
    def snapshot(self) -> Optional[TransportableFile]:
        img = self.__snapshot
        if img is None:
            base64 = self.get('snapshot')
            img = TransportableFile.parse(base64)
            self.__snapshot = img
        return img

    @snapshot.setter  # Override
    def snapshot(self, img: TransportableFile):
        self.pop('snapshot', None)
        # self['snapshot'] = None if img is None else img.serialize()
        self.__snapshot = img
