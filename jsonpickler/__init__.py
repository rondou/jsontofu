# -*- coding: utf-8 -*-
import jsonpickle
import json
from typing import Any, Callable, Dict, List, Optional, Union, NewType, Iterable, TypeVar

T = TypeVar('T')

def _type_full_name(clazz: Any) -> str:
    return ".".join([clazz.__module__, clazz.__name__])

def decode(res: Any, clazz: Any) -> T:
    res = json.loads(res) if type(res) is str else res
    res['py/object'] = _type_full_name(clazz)

    obj = jsonpickle.decode(json.dumps(res))
    for prop, value in vars(obj).items():
        if type(value) is list:
            for i, v in enumerate(value):
                arg_clazz = clazz.__annotations__[prop].__args__[0]
                value[i] = decode(v, arg_clazz)

        if type(value) is dict:
            prop_clazz = clazz.__annotations__[prop]
            if (prop_clazz is Any): continue
            if (prop_clazz is List): continue
            obj.__setattr__(prop, decode(value, prop_clazz))

    return obj
