from pytest import raises

from voluptuous import Schema, MultipleInvalid, Coerce, Optional, UNDEFINED, Required

from typedtuple import typedtuple, schema, TypedTupleType

from math import sqrt

from collections import OrderedDict


Vector2D = typedtuple('Vector2D', {'x': float, 'y': float})


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

    Vector = typedtuple('Vector', Schema({'x': float, 'y': float}, required=True))

    with raises(MultipleInvalid):
        Vector(x=10.0)


def test_using_voluptuous():

    Vector = typedtuple('Vector', {'x': Coerce(float), 'y': Coerce(float)})

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
        vector_type = typedtuple('OrderedVector{}'.format(i), OrderedDict((
            ('x', float),
            ('y', float),
            ('z', float),
        )))
        vector_type._fields == ('x', 'y', 'z')


def test_asdict_remove_optional():

    T = typedtuple('T', {'required': int, Optional('optional'): int})

    t0 = T(required=1, optional=2)
    assert t0.required == 1
    assert t0.optional == 2

    t1 = T(required=1)
    assert t1.required == 1
    assert t1.optional == UNDEFINED

    d = t1._asdict()
    assert d['required'] == 1
    assert 'optional' not in d


def test_default_value():

    T = typedtuple('T', {
        Required('required', default=10): int,
        Optional('optional', default=100): int}
    )

    t = T()
    assert t.required == 10
    assert t.optional == 100


def test_typecheck():

    assert issubclass(Vector2D, TypedTupleType)
    assert issubclass(Vector3D, TypedTupleType)

    v0 = Vector2D(x=10.0, y=20.0)
    assert isinstance(v0, TypedTupleType)

    v1 = Vector3D(x=10.0, y=20.0, z=30.0)
    assert isinstance(v1, TypedTupleType)
