# descriptor

```python
import datetime
import json
import typing

from descriptor import validator
from descriptor.base import Field, ValidatableField, TransientField
from descriptor.error import FieldSetError
from descriptor.support.base import BaseDecoder
from descriptor.support.interface import Serializable
from descriptor.support.json import JSONEncoder, HookFactory


class SubType(Serializable):
    d: int = Field('d')


class DataTest(Serializable):
    a: int = Field('a', 'aaa')
    b: float = ValidatableField('b', '1.1 ≤ bbb ≤ 10').add_validator(validator.MaxMinValidator(1.1, 10))
    c: str = ValidatableField('c', 'ccc not blank').add_validator(validator.NotBlankValidator())
    d: datetime.timedelta = TransientField('d', 'Need to check')
    e: bool = Field('e', 'none')
    f: datetime.datetime = Field('f')
    g: typing.Union[str, int, float] = Field('g')
    h: typing.Optional[typing.Callable[[int], str]] = Field('h')
    i: typing.Any = Field('i')
    j: SubType = Field('j')

    def __init__(self):
        self.a = 1
        self.b = 2.1
        self.d = datetime.datetime.now() - datetime.datetime.min
        self.c = 'c'
        self.f = datetime.datetime.now()
        self.g = 3
        self.h = None
        self.i = {'t': 12}
        self.j = SubType()
        self.j.d = 2


def h(_h: int) -> str:
    return str(_h)


class JSONEncoderTest(JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(o)


class JSONDecoderTest(BaseDecoder):

    def _default(self, t: typing.Union[type, typing.Any], val: typing.Any) -> typing.Any:
        if isinstance(t, type):
            if issubclass(t, datetime.datetime) and isinstance(val, str):
                return datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
        return super()._default(t, val)


print(json.dumps(DataTest(), cls=JSONEncoderTest))
# 此处解析多层结构时会出现问题
from_hook = json.loads('{"a": 1, "b": 2.1, "c": "c", "f": "2021-12-08 21:53:26", "g": 3, "h": null, "i": 2}',
                       object_hook=HookFactory.make_hook(JSONDecoderTest(DataTest)))
print(JSONEncoderTest().encode(from_hook))
print(json.dumps(from_hook, cls=JSONEncoderTest))
# 多层结构不能使用object_hook
form_decoder = JSONDecoderTest(DataTest).decode(json.loads(
    '{"a": 1, "b": 2.1, "c": "c", "f": "2021-12-08 21:53:26", "g": 3, "i": {"t": 12}, "j": {"d": 2}}'))
print(JSONEncoderTest().encode(form_decoder))
print(json.dumps(form_decoder, cls=JSONEncoderTest))
try:
    DataTest().b = 100.
except FieldSetError as e:
    print(repr(e))
try:
    DataTest().c = 100
except FieldSetError as e:
    print(repr(e))
try:
    DataTest().c = '  '
except FieldSetError as e:
    print(repr(e))
DataTest().g = 2.
DataTest().g = "3"
try:
    DataTest().g = None
except FieldSetError as e:
    print(repr(e))
d = DataTest()
d.h = h
print(d.h(1))
try:
    DataTest().h = 1
except FieldSetError as e:
    print(repr(e))
d.i = None
d.i = 223
d.i = "123"
```
