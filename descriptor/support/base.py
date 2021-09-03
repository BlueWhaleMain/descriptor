import typing

from descriptor.base import TransientField
from descriptor.support.error import UnknownParameterError, ParameterTypeError
from descriptor.support.interface import Serializable, Verifiable, Encoder, Decoder
from descriptor.util import ga_get, annotation_prefix_get


class _NotSet:
    pass


class BaseEncoder(Encoder[typing.Any, typing.Any]):

    def encode(self, obj: typing.Any) -> typing.Any:
        if isinstance(obj, Serializable):
            t = type(obj)
            annotations = getattr(t, '__annotations__', {})
            result = {}
            for k in annotations:
                if isinstance(getattr(t, k, None), TransientField):
                    continue
                v = _NotSet
                try:
                    v = getattr(obj, k)
                except AttributeError:
                    pass
                if v is not _NotSet:
                    result[k] = self.encode(v)
            return result
        return obj


class BaseDecoder(Decoder[typing.Any, typing.Any]):
    def __init__(self, t: typing.Optional[type]):
        self._cls: typing.Optional[type] = t
        self._stack: typing.List[str] = []

    def decode(self, data: typing.Any) -> typing.Any:
        self._stack.clear()
        return self._default(self._cls, data)

    def _default(self, t: typing.Optional[type], val: typing.Any) -> typing.Any:
        # 嵌套处理
        t, args = ga_get(t)
        if issubclass(t, Serializable):
            if isinstance(val, dict):
                instance = t()
                annotations: typing.Dict[str, typing.Any] = getattr(t, '__annotations__', {})
                for k, v in val.items():
                    try:
                        if isinstance(annotation_prefix_get(t, k), TransientField):
                            continue
                    except AttributeError:
                        pass
                    self._stack.append(f'.{k}')
                    if annotations and k in annotations:
                        v = self._default(annotations.get(k), v)
                    else:
                        try:
                            # 未定义的字段只有在__init__初始化了值才能获取到
                            v = self._default(type(getattr(instance, k)), v)
                        except AttributeError as e:
                            raise UnknownParameterError(''.join(self._stack), e)
                    setattr(instance, k, v)
                    self._stack.pop()
                if isinstance(instance, Verifiable):
                    instance.verify()
                return instance
            self._stack.append(f'<@{t.__name__}>')
            raise ParameterTypeError(''.join(self._stack), type(val))
        if args:
            if isinstance(val, dict) and len(args) == 2:
                result = t()
                for k, v in val.items():
                    lc, _ = ga_get(args[0])
                    rc, _ = ga_get(args[1])
                    self._stack.append(f'.{k}')
                    result[self._default(args[0], k)] = self._default(args[1], k)
                    self._stack.pop()
                return result
            if isinstance(val, list) and len(args) == 1:
                result = t()
                for i in range(len(val)):
                    cls, _ = ga_get(args[0])
                    self._stack.append(f'[{i}]')
                    result.append(self._default(args[0], val[i]))
                    self._stack.pop()
                return result
            self._stack.append(f'<!{t.__name__}<{",".join("?" * len(args))}>>')
            raise ParameterTypeError(''.join(self._stack), type(val))
        if isinstance(val, t):
            return val
        self._stack.append(f'<{t.__name__}>')
        raise ParameterTypeError(''.join(self._stack), type(val))
