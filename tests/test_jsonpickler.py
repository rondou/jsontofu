# -*- coding: utf-8 -*-

from dataclasses import dataclass
import jsonpickler

from typing import Any, Callable, Dict, List, Optional, Union, NewType, Iterable, TypeVar


@dataclass
class Data:
    test_str: str
    test_int: int

@dataclass
class ListData:
    test_str: str
    test_list: List[Data]

def test_empty():
    obj = jsonpickler.decode('''{}''', Data)

    assert obj is not None

def test_invalid():
    try:
        obj = jsonpickler.decode('''{''', Data)
    except:
        assert True
    else:
        assert False

def test_int_str():
    obj = jsonpickler.decode('''{"test_str": "test", "test_int": 123}''', Data)

    assert obj.test_str == 'test'
    assert obj.test_int == 123


def test_list():
    obj = jsonpickler.decode('''{"test_str": "test", "test_list": [{"test_str": "abc", "test_int": 11}]}''', ListData)

    assert obj == ListData(test_str="test", test_list=[Data(test_str="abc", test_int=11)])
