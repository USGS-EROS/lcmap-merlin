from cytoolz import cons
from cytoolz import merge
from merlin import specs
from merlin.support import data as d


def test_only():
    registry = [{'key': 1, 'ubid': 'a'}, {'key': 2, 'ubid': 'b'},
                {'key': 3, 'ubid': 'c'}, {'key': 4, 'ubid': 'd'}]

    expected = tuple([{'key': 1, 'ubid': 'a'}, {'key': 4, 'ubid': 'd'}])
    result   = specs.only(ubids=['a', 'd'], specs=registry)
    assert expected == result

    expected = tuple([{'key': 1, 'ubid': 'a'}, {'key': 4, 'ubid': 'd'}])
    result   = specs.only(ubids=['d', 'a'], specs=registry)
    assert expected == result
    
    expected = tuple()
    result = specs.only(ubids=['z'], specs=registry)
    assert expected == result


def test_mapped():
    registry = [{'key': 1, 'ubid': 'a'}, {'key': 2, 'ubid': 'b'},
                {'key': 3, 'ubid': 'c'}, {'key': 4, 'ubid': 'd'}]

    ubids = {'red': ['a', 'd'], 'blue': ['b', 'c']}

    expected = {'red':  ({'key': 1, 'ubid': 'a'}, {'key': 4, 'ubid': 'd'}),
                'blue': ({'key': 2, 'ubid': 'b'}, {'key': 3, 'ubid': 'c'})}
                
    result = specs.mapped(ubids=ubids, specs=registry)
    assert expected == result


def test_exist():
    registry = [{'key': 1, 'ubid': 'a'}, {'key': 2, 'ubid': 'b'},
                {'key': 3, 'ubid': 'c'}, {'key': 4, 'ubid': 'd'}]

    ubids = ['a', 'd']
    assert True==specs.exist(ubids=ubids, specs=registry)

    ubids = ['a', 'b', 'x']
    assert False==specs.exist(ubids=ubids, specs=registry)

    
def test_byubid():
    registry = [{'key': 1, 'ubid': 'a'}, {'key': 2, 'ubid': 'b'},
                {'key': 3, 'ubid': 'c'}, {'key': 4, 'ubid': 'd'}]
    
    results = specs.byubid(registry)

    # check that dicts were rekeyed into a new dict
    assert all(map(lambda r: r in results, ['a', 'b', 'c', 'd']))

    # check structure of new dict values
    assert all(map(lambda r: 'ubid' in r and 'key' in r, results.values()))


def test_ubids():
    registry = [{'key': 1, 'ubid': 'a'}, {'key': 2, 'ubid': 'b'},
                {'key': 3, 'ubid': 'c'}, {'key': 4, 'ubid': 'd'}]

    data = list(cons({'nope': 'z'}, registry))

    good = filter(lambda f: 'ubid' in f, data)
    
    assert set(map(lambda u: u['ubid'], good)) == set(specs.ubids(data))


def test_ubids_from_chip_specs():
    assert len(specs.ubids(d.chip_specs('blue'))) == 4


def test_refspec():
    specmap = {'red':  [{'key': 1, 'ubid': 'a'}, {'key': 2, 'ubid': 'b'}],
               'blue': [{'key': 3, 'ubid': 'c'}, {'key': 4, 'ubid': 'd'}]}

    assert type(specs.refspec(specmap)) is dict
