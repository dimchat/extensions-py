# DIM Application eXtensions (Python)

[![License](https://img.shields.io/github/license/dimchat/extensions-py)](https://github.com/dimchat/extensions-py/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/dimchat/extensions-py/pulls)
[![Platform](https://img.shields.io/badge/Platform-Python%203-brightgreen.svg)](https://github.com/dimchat/extensions-py/wiki)
[![Issues](https://img.shields.io/github/issues/dimchat/extensions-py)](https://github.com/dimchat/extensions-py/issues)
[![Repo Size](https://img.shields.io/github/repo-size/dimchat/extensions-py)](https://github.com/dimchat/extensions-py/archive/refs/heads/master.zip)
[![Tags](https://img.shields.io/github/tag/dimchat/extensions-py)](https://github.com/dimchat/extensions-py/tags)
[![Version](https://img.shields.io/pypi/v/dimax)](https://pypi.org/project/dimax)

[![Watchers](https://img.shields.io/github/watchers/dimchat/extensions-py)](https://github.com/dimchat/extensions-py/watchers)
[![Forks](https://img.shields.io/github/forks/dimchat/extensions-py)](https://github.com/dimchat/extensions-py/forks)
[![Stars](https://img.shields.io/github/stars/dimchat/extensions-py)](https://github.com/dimchat/extensions-py/stargazers)
[![Followers](https://img.shields.io/github/followers/dimchat)](https://github.com/orgs/dimchat/followers)

## Dependencies

* Latest Versions

| Name | Version | Description |
|------|---------|-------------|
| [Ming Ke Ming (名可名)](https://github.com/dimchat/mkm-py) | [![Version](https://img.shields.io/pypi/v/mkm)](https://pypi.org/project/mkm) | Decentralized User Identity Authentication |
| [Dao Ke Dao (道可道)](https://github.com/dimchat/dkd-py) | [![Version](https://img.shields.io/pypi/v/dkd)](https://pypi.org/project/dkd) | Universal Message Module |
| [DIMP (去中心化通讯协议)](https://github.com/dimchat/core-py) | [![Version](https://img.shields.io/pypi/v/dimp)](https://pypi.org/project/dimp) | Decentralized Instant Messaging Protocol |

## Extensions

1. Account
   * Address
       * BTC
       * ETH
   * Meta
       * MKM _(Default)_
       * BTC
       * ETH
   * Document
       * Visa _(User)_
       * Profile
       * Bulletin _(Group)_
2. Message Contents
   * Text Content
   * File Content
       * Image Content
       * Audio Content
       * Video Content
   * Page Content
   * Name Card
   * Quote Content
   * Money Content
       * Transfer Money
   * Combine Forward
3. System Commands
   * Meta Command
   * Document Command
   * Receipt Command
   * History Command
   * Group Command
       * Invite
       * Expel
       * Query
       * Quit
       * Join

## Examples

### Address

```python
from typing import Optional

from dimp import Address, ConstantString

from dimax import BaseAddressFactory
from dimax.mem.ext import address_cache


class CompatibleAddressFactory(BaseAddressFactory):
    """Address factory with a fallback for unsupported address types."""

    # Call it when received 'UIApplicationDidReceiveMemoryWarningNotification',
    # this will remove 50% of cached objects
    #
    # :return number of survivors
    def reduce_memory(self) -> int:
        cache = address_cache()
        return cache.reduce_memory()

    # Override
    def _parse(self, address: str) -> Optional[Address]:
        try:
            res = super()._parse(address=address)
            if res is not None:
                return res
        except AssertionError as error:
            # FIXME:
            raise AssertionError('invalid address: %s, error: %s' % (address, error))
        #
        #  TODO: parse for other types of address
        #
        length = len(address)
        if 4 <= length <= 64:
            return UnknownAddress(string=address)
        raise ValueError('invalid address: %s' % address)


# Unsupported Address
# ~~~~~~~~~~~~~~~~~~~
class UnknownAddress(ConstantString, Address):
    """A fallback Address for strings not recognised by any factory."""

    def __init__(self, string: str):
        super().__init__(string=string)

    @property  # Override
    def network(self) -> int:
        return 0  # EntityType.USER
```

### Meta

```python
from typing import Optional

from dimp import StrMap, Meta

from dimax import BaseMetaFactory, DefaultMeta, BTCMeta, ETHMeta
from dimax.mkm.meta_factory import doc_helper
from dimax.protocol import MetaType


class CompatibleMetaFactory(BaseMetaFactory):
    """Meta factory that dispatches by version string (mkm/btc/eth)."""

    # Override
    def parse_meta(self, meta: StrMap) -> Optional[Meta]:
        helper = doc_helper()
        version = helper.get_meta_type(meta=meta)
        if version in (MetaType.MKM, 'mkm', 'MKM'):
            out = DefaultMeta(meta=meta)
        elif version in (MetaType.BTC, 'btc', 'BTC'):
            out = BTCMeta(meta=meta)
        elif version in (MetaType.ETH, 'eth', 'ETH'):
            out = ETHMeta(meta=meta)
        else:
            # TODO: other types of meta
            raise TypeError('unknown meta type: %s' % version)
        return out if out.is_valid else None
```

### ExtensionLoader

```python
from dimp import Address, Meta, Content, Command
from dimp import ContentType

from dimax import ExtensionLoader, ContentParser, CommandParser
from dimax.protocol import MetaType

from .compat.address import CompatibleAddressFactory
from .compat.meta import CompatibleMetaFactory


# Extensions Loader
# ~~~~~~~~~~~~~~~~~
class CommonExtensionLoader(ExtensionLoader):

    # Override
    def register_address_factory(self):

        Address.set_factory(factory=CompatibleAddressFactory())

    # Override
    def register_meta_factories(self):

        mkm = CompatibleMetaFactory(version=MetaType.MKM)
        btc = CompatibleMetaFactory(version=MetaType.BTC)
        eth = CompatibleMetaFactory(version=MetaType.ETH)

        Meta.set_factory(version=MetaType.MKM, factory=mkm)
        Meta.set_factory(version=MetaType.BTC, factory=btc)
        Meta.set_factory(version=MetaType.ETH, factory=eth)

    # Override
    def register_content_factories(self):
        super().register_content_factories()

        # Application Customized
        factory = ContentParser(content_class=AppCustomizedContent)
        Content.set_factory(msg_type=ContentType.APPLICATION, factory=factory)
        Content.set_factory(msg_type=ContentType.CUSTOMIZED, factory=factory)

    # Override
    def register_command_factories(self):
        super().register_command_factories()

        # Handshake
        Command.set_factory(cmd=HandshakeCommand.HANDSHAKE,
                            factory=CommandParser(command_class=BaseHandshakeCommand))
```

> NOTE: `AppCustomizedContent`, `HandshakeCommand` and `BaseHandshakeCommand` are
> application-level classes (like the dart `protocol/customized.dart` and
> `protocol/handshake.dart`); they are not shipped in `dimax`. The registration
> primitives shown here — `ContentParser`, `CommandParser`, `Content.set_factory`,
> `Command.set_factory` and `ContentType.APPLICATION` / `ContentType.CUSTOMIZED` —
> are all real.

You must ensure that every ```Address``` you extend has a ```Meta``` type that can correspond to it one by one.

----

Copyright &copy; 2018-2026 Albert Moky
[![Followers](https://img.shields.io/github/followers/moky)](https://github.com/moky?tab=followers)
