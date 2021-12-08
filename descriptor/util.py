# -*- coding: utf-8 -*-
# Copyright by BlueWhale. All Rights Reserved.
import typing


def ga_get(t: typing.Union[type, typing.Any]) -> typing.Tuple[type, tuple]:
    """  Obtain generic alias. """
    ta = typing.get_args(t)
    if not isinstance(t, type):
        t = typing.get_origin(t)
    if t is not None:
        return t, ta
    raise TypeError(t)


def ga_chk(tl: typing.Union[type, typing.Any], tr: typing.Union[type, typing.Any]) -> typing.Tuple[type, tuple]:
    """ generic alias check """
    tl, tla = ga_get(tl)
    tr, tra = ga_get(tr)
    if issubclass(tl, tr):
        for la in tla:
            for ra in tra:
                if not issubclass(la, ra):
                    raise TypeError(la)
        return tr, tra
    raise TypeError(tl)


def ga_instance_get(val: typing.Any) -> typing.Tuple[type, tuple]:
    """ Obtain generic alias of compatible instance. """
    try:
        return ga_get(val)
    except TypeError:
        try:
            return ga_get(type(val))
        except TypeError:
            return type(val), typing.get_args(val)


_function_type = type(ga_get)


def ga_instance_chk(val: typing.Any, t: typing.Union[type, typing.Any]) -> bool:
    """ generic instance check """
    # Any无法获取到类型因为没有[]
    if t is typing.Any:
        return True
    t, args = ga_get(t)
    if t is typing.Union:
        for xt in args:
            if ga_instance_chk(val, xt):
                break
        else:
            return False
    elif t is typing.Callable:
        if isinstance(val, _function_type):
            return True
    elif not isinstance(val, t):
        return False
    if isinstance(val, dict) and len(args) == 2:
        for k, v in val.items():
            if not ga_instance_chk(k, args[0]):
                return False
            if not ga_instance_chk(v, args[1]):
                return False
    elif isinstance(val, (list, tuple, set)) and len(args) == 1:
        for x in val:
            if not ga_instance_chk(x, args[0]):
                return False
    return True


def annotation_get(cls: type, attr_name: str) -> typing.Union[type, typing.Any]:
    _cls = cls
    while True:
        try:
            return cls.__annotations__[attr_name]
        except (AttributeError, KeyError):
            if cls == object:
                raise AttributeError(f'{_cls!r} has no annotation {attr_name!r}!')
            cls = cls.__base__


def annotation_prefix_get(cls: type, attr_name: str) -> typing.Any:
    _cls = cls
    while True:
        try:
            _ = cls.__annotations__[attr_name]
            return cls.__dict__[attr_name]
        except (AttributeError, KeyError):
            if cls == object:
                raise AttributeError(f'{_cls!r} has no annotation {attr_name!r}!')
            cls = cls.__base__
