# -*- coding: utf-8 -*-
# Copyright by BlueWhale. All Rights Reserved.


class ValidateError(ValueError):
    def __init__(self, val, msg: str, *args):
        super().__init__(val, msg, *args)
        self.__val = val
        self.__msg = msg

    @property
    def val(self):
        return self.__val

    @property
    def msg(self):
        return self.__msg


class FieldSetError(RuntimeError):
    def __init__(self, field_name: str, val, msg: str, *args):
        super().__init__(field_name, val, msg, *args)
        self.__field_name = field_name
        self.__val = val
        self.__msg = msg

    @property
    def field_name(self):
        return self.__field_name

    @property
    def val(self):
        return self.__val

    @property
    def msg(self):
        return self.__msg
