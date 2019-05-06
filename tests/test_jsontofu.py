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
class ListData2:
    test_str: str
    test_list: List

@dataclass
class DictData:
    test_str: str
    test_dict: Optional[Dict]

@dataclass
class OptionalData:
    test_str: str
    data: Optional[Data] = None

@dataclass
class NestedData:
    test_str: str
    data: Data = Any

@dataclass
class UserAccount:
    user_id: str
    account_id: str
    location_id: str
    group_id: str

@dataclass
class Meta:
    type: str
    func: str
    rtype: str
    concurrent: bool
    args: Optional[List] = None
    kwargs: Optional[Dict] = None

@dataclass
class UserInfo:
    account: UserAccount

class MetaNone:
    ty: str
    func: Optional[str] = None
    cmd: Optional[str] = None
    concurrent: Optional[bool] = None
    rtype: Optional[str] = 'json'
    path: Optional[str] = None
    args: Optional[List] = None
    kwargs: Optional[Dict] = None

    def __init__(self,
                ty: str,
                func: Optional[str] = None,
                cmd: Optional[str] = None,
                concurrent: Optional[bool] = None,
                rtype: Optional[str] = 'json',
                path: Optional[str] = None,
                args: Optional[List] = None,
                kwargs: Optional[Dict] = None):

        self.ty = ty
        self.func = func
        self.concurrent = concurrent
        self.rtype = rtype
        self.path = path
        self.args = args
        self.kwargs = kwargs

@dataclass
class MetaLostKey:
    type: str
    func: str
    rtype: str


def test_dict_nokey():
    obj = jsontofu.decode('''{"test_str": "test",
                              "data": {"test_str": "abc", "test_int": 11, "more_key": 22}}''', OptionalData)

    assert not hasattr(obj.data, 'more_key')


def test_list_nokey():
    obj = jsontofu.decode('''{"test_str": "test",
                              "test_list": [{"test_str": "abc", "test_int": 11, "more_key": 22}]}''', ListData)

    assert not hasattr(obj.test_list[0], 'more_key')
    assert obj == ListData(test_str="test", test_list=[Data(test_str="abc", test_int=11)])


def test_nokey():
    obj = jsontofu.decode('''{"type": "built_in", "func": "memory_info", "rtype": "json", "concurrent": false}''', MetaLostKey)
    assert obj.type == "built_in"
    assert not hasattr(obj, 'concurrent')


def test_no_dataclass():
    obj = jsontofu.decode('''{
      "ty": "shell",
      "func": "memory_info",
      "args": [],
      "kwargs": {},
      "rtype": "string",
      "concurrent": true
    }''', MetaNone)

    obj2 = jsontofu.decode('''{
      "ty": "built_in",
      "func": "memory_info",
      "cmd": "aux",
      "args": [],
      "kwargs": {},
      "rtype": "json",
      "path": "/root/home",
      "concurrent": true
    }''', MetaNone)

    assert obj.cmd == None
    assert obj.func == obj2.func
    assert obj.args == obj2.args
    assert obj.kwargs == None
    assert obj.ty == "shell"
    assert obj.rtype == "string"
    assert obj.concurrent == True
    assert obj.path != "/root/home"

    assert obj2.cmd == "aux"
    assert obj2.path == "/root/home"
    assert obj2.rtype == "json"
    assert obj2.rtype != obj.rtype
    assert obj2.ty == "built_in"

def test_meta():
    obj = jsontofu.decode('''{"type": "built_in", "func": "memory_info", "args": [1, 2, 3], "kwargs": {"a": "123"}, "rtype": "json", "concurrent": false}''', Meta)
    assert obj == Meta(type='built_in', func='memory_info', rtype='json', concurrent=False, args=[1, 2, 3], kwargs={'a': '123'})
    obj = jsontofu.decode('''{"type": "built_in", "func": "memory_info", "args": [1, 2, 3], "rtype": "json", "concurrent": false}''', Meta)
    assert obj == Meta(type='built_in', func='memory_info', rtype='json', concurrent=False, args=[1, 2, 3], kwargs=None)
    obj = jsontofu.decode('''{"type": "built_in", "func": "memory_info", "kwargs": {"a": "123"}, "rtype": "json", "concurrent": false}''', Meta)
    assert obj == Meta(type='built_in', func='memory_info', rtype='json', concurrent=False, args=None, kwargs={'a': '123'})
    obj = jsontofu.decode('''{"type": "built_in", "func": "memory_info", "args": [], "kwargs": {}, "rtype": "json", "concurrent": false}''', Meta)
    assert obj == Meta(type='built_in', func='memory_info', rtype='json', concurrent=False, args=[], kwargs=None)

def test_dict_obj():
    obj = jsontofu.decode('''{"account": {"user_id": "12", "account_id": "34", "location_id": "56", "group_id": "78"}}''', UserInfo)

    assert obj == UserInfo(account=UserAccount(user_id='12', account_id='34', location_id='56', group_id='78'))

def test_empty():
    obj = jsontofu.decode('''{}''', Data)

    assert obj is None

def test_normal_dict():
    obj = jsontofu.decode('''{"test_str": "data", "test_dict": {"g": "h", "v": "w"}}''', DictData)

    assert obj == DictData(test_str="data", test_dict={"g": "h", "v": "w"})

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

def test_optional2():
    obj = jsontofu.decode('''{"test_str": "test", "data":{"test_str": "nm", "test_int": 1}}''', OptionalData)

    assert obj == OptionalData(test_str='test', data=Data(test_str='nm', test_int=1))


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

def test_list2():
    obj = jsontofu.decode('''{"test_str": "test", "test_list": ["1", 1, true]}''', ListData2)
    assert obj == ListData2(test_str="test", test_list=["1", 1, True])

def test_list():
    obj = jsontofu.decode('''{"test_str": "test", "test_list": [{"test_str": "abc", "test_int": 11}]}''', ListData)

    assert obj == ListData(test_str="test", test_list=[Data(test_str="abc", test_int=11)])

def test_type_check_str():
    try:
        jsontofu.decode('''{"test_str": 0, "test_list": [{"test_str": "abc", "test_int": 11}]}''', ListData)
    except:
        assert True
    else:
        assert False

def test_type_check_int():
    try:
        jsontofu.decode('''{"test_str": "test", "test_list": [{"test_str": "abc", "test_int": ""}]}''', ListData)
    except:
        assert True
    else:
        assert False

def test_encode():
    frozen = jsontofu.encode(jsontofu.decode('''{"test_str": "test", "test_int": 123}''', Data))
    assert frozen == {"test_str": "test", "test_int": 123}

    frozen = jsontofu.encode(jsontofu.decode('''{"account": {"user_id": "12", "account_id": "34", "location_id": "56", "group_id": "78"}}''', UserInfo))
    assert frozen == {"account": {"user_id": "12", "account_id": "34", "location_id": "56", "group_id": "78"}}

    frozen = jsontofu.encode(jsontofu.decode('''{"test_str": "test", "test_list": [{"test_str": "abc", "test_int": 11}]}''', ListData))
    assert frozen == {"test_str": "test", "test_list": [{"test_str": "abc", "test_int": 11}]}

    frozen = jsontofu.encode(jsontofu.decode('''{"test_str": "test", "test_list": ["1", 1, true]}''', ListData2))
    assert frozen == {"test_str": "test", "test_list": ["1", 1, True]}

    frozen = jsontofu.encode(jsontofu.decode('''{"test_str": "test", "data":{"test_str": "nm", "test_int": 1}}''', OptionalData))
    assert frozen == {"test_str": "test", "data":{"test_str": "nm", "test_int": 1}}

    frozen = jsontofu.encode(jsontofu.decode('''{"type": "built_in", "func": "memory_info", "args": [1, 2, 3], "kwargs": {"a": "123"}, "rtype": "json", "concurrent": false}''', Meta))
    assert frozen == {"type": "built_in", "func": "memory_info", "args": [1, 2, 3], "kwargs": {"a": "123"}, "rtype": "json", "concurrent": False}
