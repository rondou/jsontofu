# -*- coding: utf-8 -*-

from dataclasses import dataclass
import jsontofu

from typing import Any, Callable, Dict, List, Optional, Union, NewType, Iterable, TypeVar


@dataclass
class Data:
    test_str: str
    test_int: int

@dataclass
class ListData:
    test_str: str
    test_list: List[Data]

@dataclass
class OptionalData:
    test_str: str
    data: Optional[Data] = None

@dataclass
class NestedData:
    test_str: str
    data: Data = Any

def test_empty():
    obj = jsontofu.decode('''{}''', Data)

    assert obj is None

def test_nested():
    obj = jsontofu.decode('''{"test_str": "data", "data": {}}''', NestedData)
    # best spec
    #try:
    #    obj != NestedData(test_str="test", data=Data(test_str="test", test_int=0))
    #except:
    #    assert True
    #else:
    #    assert False
    # ok spec
    assert obj != NestedData(test_str="data", data=Data(test_str="test", test_int=0))
    assert obj == NestedData(test_str="data", data=None)
    assert obj != NestedData(test_str="data")
    assert True

def test_optional():
    obj = jsontofu.decode('''{"test_str": "test"}''', OptionalData)
    obj2 = OptionalData(test_str="test")

    assert obj == obj2

def test_optional_empty():
    obj = jsontofu.decode('''{"test_str": "test", "data": {}}''', OptionalData)
    # best spec
    #assert obj != OptionalData(test_str="test")
    #assert obj == OptionalData(test_str="test", data={})
    #assert obj != OptionalData(test_str="test", data=None)
    # ok spec
    assert obj == OptionalData(test_str="test")
    assert obj != OptionalData(test_str="test", data={})
    assert obj == OptionalData(test_str="test", data=None)

def test_invalid():
    try:
        obj = jsontofu.decode('''{''', Data)
    except:
        assert True
    else:
        assert False

def test_int_str():
    obj = jsontofu.decode('''{"test_str": "test", "test_int": 123}''', Data)

    assert obj.test_str == 'test'
    assert obj.test_int == 123


def test_list():
    obj = jsontofu.decode('''{"test_str": "test", "test_list": [{"test_str": "abc", "test_int": 11}]}''', ListData)

    assert obj == ListData(test_str="test", test_list=[Data(test_str="abc", test_int=11)])
