# -*- coding: utf-8 -*-
# Copyright by BlueWhale. All Rights Reserved.
import typing


class Serializable:
    """ 可序列化 """


class Verifiable:
    """ 可验证（完整性） """

    def verify(self) -> None:
        """ 验证字段值是否符合规范 """
        raise NotImplementedError


_EIT = typing.TypeVar("_EIT")
_EOT = typing.TypeVar("_EOT")


class Encoder(typing.Generic[_EIT, _EOT]):
    """ 编码器 """

    def encode(self, obj: _EIT) -> _EOT:
        """ 编码数据 """
        raise NotImplementedError


_DIT = typing.TypeVar("_DIT")
_DOT = typing.TypeVar("_DOT")


class Decoder(typing.Generic[_DIT, _DOT]):
    """ 解码器 """

    def decode(self, data: _DIT) -> _DOT:
        """ 解码 """
        raise NotImplementedError
