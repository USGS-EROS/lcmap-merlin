from merlin import timeseries
from test.mocks import aardvark as ma
import test

def test_csort():
    data = list()
    data.append({'acquired': '2015-04-01'})
    data.append({'acquired': '2017-04-01'})
    data.append({'acquired': '2017-01-01'})
    data.append({'acquired': '2016-04-01'})
    results = timeseries.sort(data)
    assert(results[0]['acquired'] > results[1]['acquired'] >
           results[2]['acquired'] > results[3]['acquired'])


def test_to_rod():
    assert 1 > 0


def test_to_pyccd():
    assert 1 > 0


def test_sort():
    assert 1 > 0


def test_pyccd():

    # data should be shaped: ( ((),{}), ((),{}), ((),{}) )
    data = timeseries.pyccd(point=(-182000, 300400),
                            specs_url='http://localhost',
                            specs_fn=ma.chip_specs,
                            chips_url='http://localhost',
                            chips_fn=ma.chips,
                            acquired='1980-01-01/2015-12-31',
                            queries=test.chip_spec_queries('http://localhost'))
    assert len(data) == 10000
    assert isinstance(data, tuple)
    assert isinstance(data[0], tuple)
    assert isinstance(data[0][0], tuple)
    assert isinstance(data[0][1], dict)
    assert len(data[0][0]) == 3
