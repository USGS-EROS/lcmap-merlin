from cytoolz import dissoc
from cytoolz import first
from cytoolz import last
from cytoolz import partial
from cytoolz import reduce
from cytoolz import sliding_window
from merlin import cfg
from merlin import chips
from merlin import create
from merlin import specs
from merlin import functions as f
#from merlin import timeseries
#from merlin.support import aardvark as ma
from operator import eq
from operator import gt
import numpy as np
import pytest
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

    
def test_create_nodata():
    x = test.x_nodata
    y = test.y_nodata
    
    

def test_create():
    # data should be shaped: ( ((chip_x, chip_y, x1, y1),{}),
    #                          ((chip_x, chip_y, x1, y2),{}), )

    # get the test profile
    profile = cfg.get(profile=test.profile, overrides=test.env)
    
    # This should fail because the test data contains additional qa chips
    with pytest.raises(Exception):
        data = create(x=test.x, y=test.y, acquired=test.acquired, cfg=profile)
                      

    # test with chexists to handle quality assymetry
    data = create(x=test.x, y=test.y, acquired=test.acquired, cfg=profile)

    # make sure we have 10000 results
    assert len(data) == 10000
    assert isinstance(data, tuple)
    assert isinstance(data[0], tuple)
    assert isinstance(data[0][0], tuple)
    assert isinstance(data[0][1], dict)

    # chip_x, chip_y, x, y.  data[0][1] is the dictionary of measurements
    assert len(data[0][0]) == 4

    # check to make sure we have equal length values and that the values
    # are not empty.  FYI -- only spot checking the first returned result
    queries = test.chip_spec_queries('http://localhost')
    lens = [len(data[0][1][item]) for item in queries]
    print("Lengths:{}".format(lens))
    assert all([eq(*x) for x in sliding_window(2, lens)]) == True

    # make sure everything isn't zero length
    assert all([gt(x, 0) for x in lens]) == True


def test_compare_timeseries_to_chip():
    
    _specs = ma.chip_specs(_queries['red'])
    _ubids = specs.ubids(_specs)
    _index = specs.index(_specs)
     
    most_recent_chip = last(sorted(ma.chips(_x, _y, _acquired, 'http://localhost', _ubids), key=lambda d: d['acquired']))
    most_recent_chip = first(chips.to_numpy(spec_index=_index,
                                            chips=[most_recent_chip]))

    time_series = create(x=_x, y=_y, acquired=_acquired, cfg=config)
                         
    # this is a 2d 100x100 array of values arranged spatially
    chip_data = most_recent_chip['data']

    # reconstruct a 2d 100x100 array of values from the most recent observation in the time series.  Idea here is it
    # should match the chip_data
    #.reshape(100, 100)
    def observation(record):
        # return x, y, value for the most recent observation in the time series
        return {'x': record[0][2], 'y': record[0][3], 'v': record[1]['red'][0]}
        
    def lookups(values):
        # need to know the array position of each value, be able to look them up
        # this is a coordinate space to array space mapping
        return  {v:i for i,v in enumerate(values)}

    def build_array(obs, x_lookups, y_lookups):
        # takes all the observations and the x/y lookup tables, returns an ndarray (float)

        # initialze an ndarray that matches the dimensions of x and y
        ar = np.zeros([len(x_lookups), len(y_lookups)], dtype=np.float)

        # populate the ndarray
        for o in obs:
            x = x_lookups.get(o['x'])
            y = y_lookups.get(o['y'])
            ar.itemset((y, x), o.get('v'))
            
        return ar
       
    observations = list(map(observation, time_series))
    xset = sorted(list(set(map(lambda a: a['x'], observations))))
    yset = sorted(list(set(map(lambda a: a['y'], observations))), reverse=True)
    suspect_data = build_array(obs=observations,
                               x_lookups=lookups(xset),
                               y_lookups=lookups(yset))

    assert np.array_equal(suspect_data, chip_data)