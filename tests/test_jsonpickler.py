# -*- coding: utf-8 -*-

from dataclasses import dataclass
import jsonpickler


@dataclass
class Data:
    test_str: str
    test_int: int


def test_int_str():
    obj = jsonpickler.decode({'test_str': 'test', 'test_int': 123}, Data)

    assert obj.test_str == 'test'
    assert obj.test_int == 123
