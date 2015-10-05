typedtuple
==========

install
-------

::

  $ pip install typedtuple

basic definition
----------------

.. code:: python

    from typedtuple import TypedTuple

    # definition dictionary is converted to voluptuous.Schema(definition_dict, required=True)
    Vector = TypedTuple('Vector', {'x': float, 'y': float, 'z': float})
    v0 = Vector(x=10.0, y=20.0, z=30.0)
    print v0.x  # 10.0
    v1 = Vector(x=10, y=20)  # raises exception

using voluptuous schema
-----------------------

.. code:: python

    from voluptuous import Schema

    # can use voluptuous.Schema as definition
    Vector = TypedTuple('Vector', Schema({'x': float, 'y': float, 'z': float}, required=True))

using @schema decorator
-----------------------

.. code:: python

    from math import sqrt
    from typedtuple import schema

    @schema({'x': float, 'y': float, 'z': float})
    class Vector(object):
        @property
        def length(self):
            return sqrt(pow(self.x, 2.0) + pow(self.y, 2.0) + pow(self.z, 2.0))

    v = Vector(x=1.0, y=2.0, z=2.0)
    print v.length  # 3.0

using voluptuous functions
--------------------------

.. code:: python

    from voluptuous import Coerce
    from typedtuple import schema

    @schema({'x': Coerce(float), 'y': Coerce(float)})
    class Vector(object):
        pass

    v0 = Vector(x=10, y='20.0')
    print v0.x  # 10.0
    print v0.y  # 20.0

using OrderedDict
-----------------

.. code:: python

    from collections import OrderedDict
    from typedtuple import schema

    @schema(OrderedDict((('x', float), ('y', float), ('z', float))))
    class Vector(object):
        pass

    print Vector._fields  # ('x', 'y', 'z')

caveat
------

TypedTuple is tuple. so...

.. code:: python

    from collections import OrderedDict
    from typedtuple import TypedTuple

    Vector0 = TypedTuple('Vector0', OrderedDict((('x', float), ('y', float))))
    Vector1 = TypedTuple('Vector1', OrderedDict((('y', float), ('x', float))))

    v0 = Vector0(x=10.0, y=20.0)
    v1 = Vector1(x=20.0, y=10.0)
    v0 == v1  # True

TODO
----

use nose for test

benchmark
