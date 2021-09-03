# -*- coding: utf-8 -*-
# Copyright by BlueWhale. All Rights Reserved.
import typing

from descriptor.base import _FT
from descriptor.error import ValidateError
from descriptor.interface import Validatable


class HasValueValidator(Validatable[_FT]):
    """ 存在值验证器，不能用在bool或类似类型的字段上 """

    def validate(self, value: _FT) -> _FT:
        if value:
            return value
        raise ValidateError(value, 'must set a value')


class SubCollectionValidator(Validatable[_FT]):
    """子集验证器，集合（包括内部元素）要能够__str__"""

    def __init__(self, collection):
        self._collection = collection

    def validate(self, value: _FT) -> _FT:
        if value in self._collection:
            return value
        raise ValidateError(value, f'{value!r} must in {self._collection!r}')

    @property
    def collection(self):
        return self._collection


class NotBlankValidator(Validatable[str]):
    """ 非空白验证器 """

    def validate(self, value: str) -> str:
        if value.strip():
            return value
        raise ValidateError(value, 'can not empty or blank')


def interval_chk(_min, value, _max, val_str: str = 'value'):
    if _min is not None and value < _min or _max is not None and value > _max:
        raise ValidateError(value, f'{"" if _min is None else f"{_min} ≤ "}'
                                   f'{val_str}'
                                   f'{"" if _max is None else f" ≤ {_max}"}')
    return value


class MaxMinValidator(Validatable[_FT]):
    """ 区间验证器 """

    def __init__(self, _min=None, _max=None):
        super().__init__()
        if _min is None and _max is None:
            raise ValueError('_min,_max', (_min, _max), 'must set a minimum or maximum')
        if _min is not None and _max is not None and _min > _max:
            raise ValueError('_min,_max', (_min, _max),
                             'the minimum value cannot be greater than the maximum value')
        self._min = _min
        self._max = _max

    def validate(self, value: _FT) -> _FT:
        return interval_chk(self.min, value, self.max)

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max


class LenValidator(Validatable[_FT]):
    """ 长度验证器 """

    def __init__(self, _min=None, _max=None):
        super().__init__()
        if _min is None and _max is None:
            raise ValueError('LenValidator:_min,_max', (_min, _max), 'must set a minimum length or maximum length')
        if _min is not None and _max is not None and _min > _max:
            raise ValueError('LenValidator:_min,_max', (_min, _max),
                             'the minimum value cannot be greater than the maximum value')
        self._min = _min
        self._max = _max

    def validate(self, value: _FT) -> _FT:
        return interval_chk(self.min, len(value), self.max, 'len(value)')

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max


class RegxValidator(Validatable[str]):
    """ 正则验证器 """

    def __init__(self, regx: typing.Pattern):
        super().__init__()
        self._regx: typing.Pattern = regx

    def validate(self, value: str) -> str:
        if self._regx.fullmatch(value):
            return value
        raise ValidateError(value, f'value must match the expression {self._regx.pattern!r}')

    @property
    def regx(self) -> typing.Pattern:
        return self._regx
