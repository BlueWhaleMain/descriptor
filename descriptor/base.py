# -*- coding: utf-8 -*-
# Copyright by BlueWhale. All Rights Reserved.
import builtins
import inspect
import typing

from descriptor.error import FieldSetError, ValidateError
from descriptor.interface import Validatable
from descriptor.util import annotation_get, ga_instance_chk

# ClassType
_CT = typing.TypeVar('_CT')
# FieldType
_FT = typing.TypeVar('_FT')


class Field(typing.Generic[_FT]):
    """ 字段（描述符） """

    def __init__(self, attr_name: str, attr_doc: str = ''):
        """ 初始化字段描述
        :param attr_name: 字段名称
        :param attr_doc: 字段文档 默认字段类型文档注释
        """
        if not attr_name:
            raise ValueError('field name must set.')
        self._attr_name = attr_name
        if attr_doc is None:
            try:
                attr_type = getattr(getattr(inspect.currentframe().f_back.f_locals, '__annotations__'), attr_name)
            except AttributeError:
                raise ValueError('use None attr_doc, must set a type annotation.')
            if inspect.getmodule(attr_type) is not builtins:
                attr_doc = attr_type.__doc__
        self.__doc__ = attr_doc

    def __get__(self, instance: _CT, owner: typing.Optional[typing.Type[_CT]]) -> _FT:
        if instance is None:
            return self
        return getattr(instance, f'_{owner.__name__}__{self.attr_name}')

    def __set__(self, instance: _CT, value: _FT):
        if instance is None:
            raise FieldSetError(self.attr_name, value, 'None type has no attribute \'__set__\'')
        if ga_instance_chk(value, annotation_get(type(instance), self.attr_name)):
            setattr(instance, f'_{type(instance).__name__}__{self.attr_name}', value)
        else:
            raise FieldSetError(self.attr_name, value, repr(type(value)))

    @property
    def attr_name(self):
        """ 字段名称 """
        return self._attr_name


class TransientField(Field[_FT]):
    """ 瞬时（不可持久化）字段 """


class ValidatableField(Field[_FT]):
    """ 可验证的字段 """

    def __init__(self, attr_name: str, attr_doc: str = ''):
        super().__init__(attr_name, attr_doc)
        self._validators: typing.Set[Validatable[_FT]] = set()

    def __set__(self, instance: _CT, value: _FT):
        if instance is None:
            raise FieldSetError(self.attr_name, value, 'None type has no attribute \'__set__\'')
        if ga_instance_chk(value, annotation_get(type(instance), self.attr_name)):
            for validator in self._validators:
                try:
                    validator.validate(value)
                except ValidateError as e:
                    raise FieldSetError(self.attr_name, e.val, e.msg)
            super().__set__(instance, value)
        else:
            raise FieldSetError(self.attr_name, value, repr(type(value)))

    @property
    def validators(self) -> typing.Set[Validatable[_FT]]:
        return self._validators.copy()

    def add_validator(self, validator: Validatable[_FT]):
        """ 添加验证器 """
        self._validators.add(validator)
        return self
