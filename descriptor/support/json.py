# -*- coding: utf-8 -*-
# Copyright by BlueWhale. All Rights Reserved.
import json

from descriptor.support.base import BaseEncoder
from descriptor.support.interface import Decoder


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        return BaseEncoder().encode(o)


class HookFactory:
    @classmethod
    def make_hook(cls, decoder: Decoder):
        def hook(d: dict):
            return decoder.decode(d)

        return hook
