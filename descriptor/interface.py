# -*- coding: utf-8 -*-
# Copyright by BlueWhale. All Rights Reserved.
import typing

_VDT = typing.TypeVar("_VDT")


class Validatable(typing.Generic[_VDT]):
    """ 可验证（单个值） """

    def validate(self, value: _VDT):
        raise NotImplementedError
