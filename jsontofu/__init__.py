# -*- coding: utf-8 -*-
import sys
import json
import jsonpickle

import typing
from typing import Any, Callable, Dict, List, Optional, Union, NewType, Iterable, TypeVar, Union

T = TypeVar('T')

def _type_full_name(clazz: Any) -> str:
    return ".".join([clazz.__module__, clazz.__name__])


def decode(res: Any, clazz: Any) -> T:
    res = json.loads(res) if type(res) is str else res

    if not res:
        return None

    uni_on = type(Union)
    if sys.version_info >= (3,7):
        uni_on = typing._GenericAlias

    if type(clazz) is uni_on:
        clazz = clazz.__args__[0]

    try:
        clazz.__name__
    except:
        return res

    res['py/object'] = _type_full_name(clazz)

    obj = jsonpickle.decode(json.dumps(res))

    if type(obj) is dict:
        obj.pop('py/object', None)
        return obj

    for prop, value in vars(obj).items():
        if type(value) is list:
            for i, v in enumerate(value):
                if type(v) is str: continue
                if type(v) is int: continue
                if type(v) is bool: continue
                if type(v) is float: continue

                arg_clazz = clazz.__annotations__[prop].__args__[0]
                value[i] = decode(v, arg_clazz)


        prop_clazz = clazz.__annotations__[prop]
        if type(value) is dict:
            if prop_clazz is Any: continue
            if prop_clazz is List: continue
            obj.__setattr__(prop, decode(value, prop_clazz))

        if prop_clazz is str:
            assert type(value) == str
        elif prop_clazz is int:
            assert type(value) == int
        elif prop_clazz is bool:
            assert type(value) == bool
        elif prop_clazz is float:
            assert type(value) == float
        #elif prop_clazz is List:
        #    assert type(value) == List
        #elif prop_clazz is list:
        #    assert type(value) == list
        #elif prop_clazz is dict:
        #    assert type(value) == dict

    return obj
