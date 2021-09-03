# -*- coding: utf-8 -*-
# Copyright by BlueWhale. All Rights Reserved.
import typing

from descriptor.support.interface import Serializable


class DataLengthError(ValueError):
    """ 数据长度异常 """

    def __init__(self, length: int, required: int, *args):
        super().__init__(f'data length required {required!r}, got {length!r}', *args)
        self.__length: int = length
        self.__required: int = required

    @property
    def length(self) -> int:
        """ 现有长度 """
        return self.__length

    @property
    def required(self) -> int:
        """ 需要长度 """
        return self.__required


class DataEncodeError(ValueError):
    """ 数据编码异常 """

    def __init__(self, obj: Serializable, msg: str = '', *args):
        super().__init__(f"data encode error{f':{msg}' if msg else '.'}", *args)
        self.__obj: Serializable = obj

    @property
    def obj(self) -> Serializable:
        """ 实体类 """
        return self.__obj


class ParameterError(AttributeError):
    """ 字段异常 """

    def __init__(self, param: str, msg: str, *args):
        super().__init__(f"parameter {param!r} error{f', {msg}' if msg else '.'}", *args)
        self.__param: str = param

    @property
    def param(self) -> str:
        """ 字段 """
        return self.__param


class UnknownParameterError(ParameterError):
    """ 未知字段异常 """

    def __init__(self, param: str, *args):
        super().__init__(param, 'unknown parameter', *args)


class ParameterTypeError(ParameterError, TypeError):
    """ 字段类型异常 """

    def __init__(self, param: str, t: typing.Type, *args):
        super().__init__(param, f'type error:{t.__name__!r}', *args)
        self.__type: typing.Type = t

    @property
    def type(self) -> typing.Type:
        """ 字段的类型 """
        return self.__type


class ParameterRequiredError(ParameterError):
    """ 需要字段异常 """

    def __init__(self, param: str, *args):
        super().__init__(param, 'required', *args)


class ParameterValueError(ParameterError, ValueError):
    """ 字段值异常 """

    def __init__(self, param: str, val, msg: str = '', *args):
        super().__init__(param, f"{f'{msg}, ' if msg else ''}{f'found {val!r}'}", *args)
        self.__val = val

    @property
    def val(self):
        """ 值 """
        return self.__val
