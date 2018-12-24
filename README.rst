.. image:: jsontofu.png

Usage
-----

.. code:: python

    @dataclass
    class Data:
        str_data: str
        int_data: int
        
    @dataclass
    class DictData:
        str_data: str
        dict_data: Optional[Dict]
        
    @dataclass
    class RecursiveData:
        str_data: str
        dict_data: Data
        
    json_data1 = {
        'str_data': 'test',
        'int_data': 123
    }
             
    json_data2 = {, 
        'str_data': 'test',
        'dict_data': {'key1': 123, 'key2': 456}
    }
        
    json_data3 = {, 
        'str_data': 'test',
        'dict_data': {'str_data': 'test', 'int_data': 456}
    }
    
    print(jsontofu.decode(json_data1, Data)) # Data(str_data="test", int_data=123)
    
    print(jsontofu.decode(json_data2, DictData)) # DictData(str_data="test", dict_data={'key1': 123, 'key2': 456})
    
    print(jsontofu.decode(json_data3, RecursiveData)) # RecursiveData(str_data="test", Data(str_data="test", int_data=456)
    

Installation
------------

.. code:: sh

    pip install git+git://github.com/rondou/jsontofu.git

or

.. code:: sh

    pipenv install 'git+ssh://git@github.com/rondou/jsontofu.git#egg=jsontofu'


Development
-----------

.. code:: sh

    pipenv install
    pipenv install -d
    pipenv run "pytest -s"

Coverage
-----------

.. code:: sh

    pipenv run 'pytest tests --cov=jsontofu'
