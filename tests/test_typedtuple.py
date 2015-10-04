from pytest import raises

from voluptuous import Schema, MultipleInvalid, Coerce

from typedtuple import TypedTuple, schema

from math import sqrt

from collections import OrderedDict


Vector2D = TypedTuple('Vector2D', {'x': float, 'y': float})


@schema({'x': float, 'y': float, 'z': float})
class Vector3D(object):
    pass


def test_definition():

    v = Vector2D(x=10.0, y=20.0)
    assert round(v.x - 10.0, 1) == 0
    assert round(v.y - 20.0, 1) == 0


def test_validation():

    with raises(MultipleInvalid):
        Vector2D(x=10.0)

    with raises(MultipleInvalid):
        Vector2D(x=10)

    with raises(MultipleInvalid):
        Vector2D(x=10.0, y=20.0, z=30.0)


def test_schema_definition():

    Vector = TypedTuple('Vector', Schema({'x': float, 'y': float}, required=True))

    with raises(MultipleInvalid):
        Vector(x=10.0)


def test_using_voluptuous():

    Vector = TypedTuple('Vector', {'x': Coerce(float), 'y': Coerce(float)})

    v0 = Vector(x=10, y=20)
    v1 = Vector(x='10.0', y='20.0')
    assert round(v0.x - 10.0, 1) == round(v1.x - 10.0, 1) == 0
    assert round(v0.y - 20.0, 1) == round(v1.y - 20.0, 1) == 0

    with raises(MultipleInvalid):
        Vector(x='a', y='b')


def test_inheritance():

    class VectorMixin(object):
        @property
        def length(self):
            return sqrt(sum(pow(x, 2.0) for x in self))

    @schema({'x': float, 'y': float})
    class Vec2D(VectorMixin):
        pass

    @schema({'x': float, 'y': float, 'z': float})
    class Vec3D(VectorMixin):
        pass

    assert round(Vec2D(x=3.0, y=4.0).length - 5.0, 1) == 0
    assert round(Vec3D(x=1.0, y=2.0, z=2.0).length - 3.0, 1) == 0


def test_inhibit_attribute_addition():

    v = Vector3D(x=10.0, y=20.0, z=30.0)
    with raises(AttributeError):
        v.w = 1.0


def test_field_order_fixing():

    for i in range(100):
        vector_type = TypedTuple('OrderedVector{}'.format(i), OrderedDict((
            ('x', float),
            ('y', float),
            ('z', float),
        )))
        vector_type._fields == ('x', 'y', 'z')
