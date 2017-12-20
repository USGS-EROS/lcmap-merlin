from base64 import b64encode
from cytoolz import drop
from merlin import chips
from merlin import specs
from functools import partial
from functools import reduce
from itertools import product
from numpy.random import randint
import numpy as np


def test_difference():
    assert chips.difference(3456, 3000) == 456
    assert chips.difference(3456, 5000) == 3456


def test_near():
    assert chips.near(2999, 3000, 0) == 0
    assert chips.near(3000, 3000, 0) == 3000
    assert chips.near(-2999, -3000, 0) == 0
    assert chips.near(-3000, -3000, 0) == -3000


def test_point_to_chip():
    assert chips.point_to_chip(2999, -2999, 3000, -3000, 0, 0) == (0, 0)
    assert chips.point_to_chip(3000, -3000, 3000, -3000, 0, 0) == (3000, -3000)


def test_snap():
    spec = {'chip_x': 3000, 'chip_y': -3000, 'shift_x': 0, 'shift_y': 0}
    assert (0, 0) == chips.snap(2999, -2999, spec)
    assert (3000, 0) == chips.snap(3000, -2999, spec)
    assert (0, -3000) == chips.snap(2999, -3000, spec)
    assert (3000, -3000) == chips.snap(3000, -3000, spec)


def test_coordinates():
    spec   = {'chip_x': 3000, 'chip_y': -3000, 'shift_x': 0, 'shift_y': 0}
    coords = ((0, 0), (0, -3000), (3000, 0), (3000, -3000))
    assert coords == chips.coordinates(0, 0, 3000, -3000, spec)


def bounds_to_coordinates():
    # fail until implemented
    assert 1 < 0


def test_locations():
    params = {'startx': 0,
              'starty': 0,
              'cw': 2,
              'ch': 2,
              'rx': 1,
              'ry': -1,
              'sx': 60,
              'sy': 60}

    locs = np.array([[[0, 0], [30, 0]], [[0, -30], [30, -30]]])
    assert np.array_equal(locs, chips.locations(**params))
    

def test_dates():
    inputs = list()
    inputs.append({'acquired': '2015-04-01'})
    inputs.append({'acquired': '2017-04-01'})
    inputs.append({'acquired': '2017-01-01'})
    inputs.append({'acquired': '2016-04-01'})
    assert set(chips.dates(inputs)) == set(map(lambda d: d['acquired'], inputs))


def test_trim():
    inputs = list()
    inputs.append({'include': True, 'acquired': '2015-04-01'})
    inputs.append({'include': True, 'acquired': '2017-04-01'})
    inputs.append({'include': False, 'acquired': '2017-01-01'})
    inputs.append({'include': True, 'acquired': '2016-04-01'})
    included = chips.dates(filter(lambda d: d['include'] is True, inputs))
    trimmed = chips.trim(dates=included, chips=inputs)
    assert len(list(trimmed)) == len(included)
    assert set(included) == set(map(lambda x: x['acquired'], trimmed))


def test_chip_to_numpy():
    # fail until implemented
    assert 1 < 0
    

def test_to_numpy():
    """ Builds combos of shapes and numpy data types and tests
        aardvark.to_numpy() with all of them """

    def _ubid(dtype, shape):
        return dtype + str(shape)

    def _chip(dtype, shape, ubid):
        limits = np.iinfo(dtype)
        length = reduce(lambda accum, v: accum * v, shape)
        matrix = randint(limits.min, limits.max, length, dtype).reshape(shape)
        return {'ubid': ubid, 'data': b64encode(matrix)}

    def _spec(dtype, shape, ubid):
        return {'ubid': ubid, 'data_shape': shape, 'data_type': dtype.upper()}

    def _check(npchip, spec_index):
        spec = spec_index[npchip['ubid']]
        assert npchip['data'].dtype.name == spec['data_type'].lower()
        assert npchip['data'].shape == spec['data_shape']
        return True

    # Test combos of dtypes/shapes to ensure data shape and type are unaltered
    combos = tuple(product(('uint8', 'uint16', 'int8', 'int16'),
                           ((3, 3), (1, 1), (100, 100))))

    # generate the chip_specs and chips
    _chips = [_chip(*c, _ubid(*c)) for c in combos]
    _specs = [_spec(*c, _ubid(*c)) for c in combos]
    _spec_index = specs.index(_specs)

    # run assertions
    checker = partial(_check, spec_index=_spec_index)
    all(map(checker, chips.to_numpy(spec_index=_spec_index, chips=_chips)))


def test_identity():
    chip = {'x': 1, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'}
    assert chips.identity(chip) == tuple([chip['x'], chip['y'],
                                          chip['ubid'], chip['acquired']])


def test_deduplicate():
    inputs = [{'x': 1, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'},
              {'x': 1, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'},
              {'x': 2, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'},
              {'x': 1, 'y': 3, 'acquired': '1980-01-01', 'ubid': 'a/b/c/d'},
              {'x': 1, 'y': 2, 'acquired': '1980-01-02', 'ubid': 'a/b/c/d'},
              {'x': 1, 'y': 2, 'acquired': '1980-01-01', 'ubid': 'a/b/c'}]

    assert chips.deduplicate(inputs) == tuple(drop(1, inputs))


def test_mapped():
    # fail until filled out
    assert 1 < 0


def test_rsort():
    # fail until tested
    assert 1 < 0
