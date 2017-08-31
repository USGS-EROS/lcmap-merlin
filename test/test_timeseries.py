from cytoolz import partial
from merlin import functions as f
from merlin import timeseries
from merlin.support import aardvark as ma
import test
import pytest


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


def test_create():
    from cytoolz import dissoc
    # data should be shaped: ( ((),{}), ((),{}), ((),{}) )
    # This should pass since we are dissoc'ing quality, which has additional
    # chips.
    data = timeseries.create(
               point=(-182000, 300400),
               specs_fn=ma.chip_specs,
               chips_url='http://localhost',
               chips_fn=ma.chips,
               acquired='1980-01-01/2015-12-31',
               queries=dissoc(test.chip_spec_queries('http://localhost'),
                              'quality'))

    assert len(data) == 10000
    assert isinstance(data, tuple)
    assert isinstance(data[0], tuple)
    assert isinstance(data[0][0], tuple)
    assert isinstance(data[0][1], dict)
    assert len(data[0][0]) == 3

    # This should fail because the test data contains additional qa chips
    with pytest.raises(Exception):
        data = timeseries.create(
                   point=(-182000, 300400),
                   specs_fn=ma.chip_specs,
                   chips_url='http://localhost',
                   chips_fn=ma.chips,
                   acquired='1980-01-01/2015-12-31',
                   queries=test.chip_spec_queries('http://localhost'))

    # test with chexists to handle quality assymetry
    data = timeseries.create(
                    point=(-182000, 300400),
                    dates_fn=partial(f.chexists,
                                     check_fn=timeseries.symmetric_dates,
                                     keys=['quality']),
                    specs_fn=ma.chip_specs,
                    chips_url='http://localhost',
                    chips_fn=ma.chips,
                    acquired='1980-01-01/2015-12-31',
                    queries=test.chip_spec_queries('http://localhost'))
