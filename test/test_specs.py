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
    inputs = list()
    inputs.append({'ubid': 'a', 'data': None})
    inputs.append({'ubid': 'b', 'data': None})
    inputs.append({'ubid': 'c', 'data': None})
    results = specs.byubid(inputs)
    # check that dicts were rekeyed into a new dict
    assert all(map(lambda r: r in results, ['a', 'b', 'c']))
    # check structure of new dict values
    assert all(map(lambda r: 'ubid' in r and 'data' in r, results.values()))


def test_ubids():
    data = ({'ubid': 'a/b/c'}, {'ubid': 'd/e/f'}, {'ubid': 'g'}, {'nope': 'z'})
    good = filter(lambda f: 'ubid' in f, data)
    assert set(map(lambda u: u['ubid'], good)) == set(specs.ubids(data))


def test_ubids_from_chip_specs():
    assert len(specs.ubids(d.chip_specs('blue'))) == 4
