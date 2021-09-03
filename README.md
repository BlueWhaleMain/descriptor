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


class DataTest(Serializable):
    a: int = Field('a', 'aaa')
    b: float = ValidatableField('b', '1.1 ≤ bbb ≤ 10').add_validator(validator.MaxMinValidator(1.1, 10))
    c: str = ValidatableField('c', 'ccc not blank').add_validator(validator.NotBlankValidator())
    d: datetime.timedelta = TransientField('d', 'Need to check')
    e: bool = Field('e', 'none')
    f: datetime.datetime = Field('f')

    def __init__(self):
        self.a = 1
        self.b = 2.1
        self.d = datetime.datetime.now() - datetime.datetime.min
        self.c = 'c'
        self.f = datetime.datetime.now()


class JSONEncoderTest(JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(o)


class JSONDecoderTest(BaseDecoder):

    def _default(self, t: typing.Optional[type], val: typing.Any) -> typing.Any:
        if issubclass(t, datetime.datetime) and isinstance(val, str):
            return datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
        return super()._default(t, val)


print(json.dumps(DataTest(), cls=JSONEncoderTest))
print(json.loads('{"a": 1, "b": 2.1, "c": "c", "f": "2021-09-03 13:57:54"}',
                 object_hook=HookFactory.make_hook(JSONDecoderTest(DataTest))))
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

```
