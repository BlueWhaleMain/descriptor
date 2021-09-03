# -*- coding: utf-8 -*-
# Copyright by BlueWhale. All Rights Reserved.
import typing


def ga_get(t: typing.Optional[type]) -> typing.Tuple[type, tuple]:
    """  Obtain generic alias. """
    try:
        # typing._GenericAlias
        ta = getattr(t, '__args__')
        t = getattr(t, '__origin__')
        return t, ta
    except AttributeError:
        pass
    if isinstance(t, type):
        return t, ()
    raise TypeError(t)


def ga_chk(tl: typing.Optional[type], tr: typing.Optional[type]) -> typing.Tuple[type, tuple]:
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
        return type(val), ()


def ga_instance_chk(val: typing.Any, t: typing.Optional[type]) -> bool:
    """ generic instance check """
    t, args = ga_get(t)
    if not isinstance(val, t):
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


def annotation_get(cls: type, attr_name: str) -> typing.Optional[type]:
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
