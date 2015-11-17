from itertools import repeat

try:
    from cnamedtuple import namedtuple
except ImportError:
    from collections import namedtuple
from collections import OrderedDict

from voluptuous import Schema, UNDEFINED

from six import iterkeys, iteritems
from six.moves import zip


def TypedTuple(name, definition):

    if isinstance(definition, Schema):
        schema = definition
        definition = definition.schema
    elif isinstance(definition, dict):
        schema = Schema(definition, required=True)
    else:
        raise ValueError('definition must be voluptuous.Schema or dict')

    nt = namedtuple(name, [str(key) for key in iterkeys(definition)])

    def new(cls, *args, **kwargs):
        kwargs.update(dict(zip(nt._fields[:len(args)], args)))
        for key in (k for k, v in iteritems(kwargs) if v is UNDEFINED):
            del kwargs[key]
        validated = schema(kwargs)
        validated.update(dict(zip((field for field in nt._fields if field not in validated), repeat(UNDEFINED))))
        return nt.__new__(cls, **validated)

    return type(name, (nt,), {
        '__new__': new,
        '_make': classmethod(lambda cls, iterable: new(cls, *iterable)),
        '_asdict': lambda self: OrderedDict(v for v in zip(self._fields, self) if v[1] != UNDEFINED),
        '__slots__': (),
    })


def schema(definition):
    def f(clazz):
        _d = dict(clazz.__dict__)
        _d['__slots__'] = ()
        return type(
            clazz.__name__,
            (type('TTProxy', clazz.__bases__, {'__slots__': ()}),) + (TypedTuple(clazz.__name__, definition),),
            _d,
        )
    return f
