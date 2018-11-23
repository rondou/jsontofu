# -*- coding: utf-8 -*-
import sys
import json
import jsonpickle

import typing
from typing import Any, Callable, Dict, List, Optional, Union, NewType, Iterable, TypeVar, Union

T = TypeVar('T')
BUILT_IN_TYPE = (str, int, bool, float)

def _type_full_name(clazz: Any) -> str:
    return ".".join([clazz.__module__, clazz.__name__])


def _get_union_type():
    union_type = type(Union)
    if sys.version_info >= (3,7):
        union_type = typing._GenericAlias

    return union_type


def _validate_match_type(res, v_type):
    if v_type in BUILT_IN_TYPE:
        assert type(res) == v_type
    #elif prop_clazz is List:
    #    assert type(value) == List
    #elif prop_clazz is list:
    #    assert type(value) == list
    #elif prop_clazz is dict:
    #    assert type(value) == dict


def _pull_out_jsonpickle_magic_key(res):
    res.pop('py/object', None)
    for k in res.keys():
        if type(res[k]) is dict:
            _pull_out_jsonpickle_magic_key(res[k])

        if type(res[k]) is list:
            for v in res[k]:
                if type(v) is dict:
                    _pull_out_jsonpickle_magic_key(v)


def encode(res: Any) -> T:
    frozen = json.loads(jsonpickle.encode(res))
    _pull_out_jsonpickle_magic_key(frozen)

    return frozen


def decode(res: Any, clazz: Any) -> T:
    res = json.loads(res) if type(res) is str else res

    if not res:
        return None

    if type(clazz) is _get_union_type():
        clazz = clazz.__args__[0]

    try:
        clazz.__name__
    except:
        return res

    res['py/object'] = _type_full_name(clazz)

    obj = jsonpickle.decode(json.dumps(res))

    if type(obj) is dict:
        _pull_out_jsonpickle_magic_key(obj)
        return obj

    for prop, value in vars(obj).items():
        if type(value) is list:
            for i, v in enumerate(value):
                if type(v) in BUILT_IN_TYPE:
                    continue

                value[i] = decode(v, clazz.__annotations__[prop].__args__[0])

        prop_clazz = clazz.__annotations__[prop]
        if type(value) is dict:
            if prop_clazz in (Any, List):
                continue
            obj.__setattr__(prop, decode(value, prop_clazz))

        _validate_match_type(value, prop_clazz)

    return obj
