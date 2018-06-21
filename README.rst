Usage
-----

.. code:: python

    @dataclass
    class Data:
        test_str: str
        test_int: int

    obj = jsontofu.decode({'test_str': 'test', 'test_int': 123}, Data)

    # Now you can call test_str like this
    obj.test_str

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
