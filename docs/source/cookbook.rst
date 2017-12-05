Cookbook
========

Create Timeseries
-------------------

.. code-block:: python3

    from merlin import chips
    from merlin import chip_specs
    import merlin

    queries = {
        'red':   'http://host/v1/landsat/chip-specs?q=tags:red AND sr',
        'green': 'http://host/v1/landsat/chip-specs?q=tags:green AND sr',
        'blue':  'http://host/v1/landsat/chip-specs?q=tags:blue AND sr'}

    timeseries = merlin.create(point=(123, 456),
                               acquired='1980-01-01/2017-01-01',
                               keyed_specs=chip_specs.getmulti(queries),
                               chips_fn=partial(chips.get, url='http://host/v1/landsat/chips'))

    print(timeseries)

    (((123, 456, 123, 456), {'red'  : [9, 8, ...],
                             'green': [99, 88, ...]},
                             'blue' : [12, 22, ...],
                              'dates': ['2017-01-01', '2016-12-31', ...]}),
     ((123, 456, 124, 456), {'red'  : [4, 3, ...],
                             'green': [19, 8, ...]},
                             'blue' : [1, 11, ...],
                             'dates': ['2017-01-01', '2016-12-31', ...]}),)

Create Timeseries From Assymetric Data
--------------------------------------
.. code-block:: python3

    from functools import partial
    from merlin import chips
    from merlin import chip_specs
    from merlin import functions
    from merlin import timeseries
    import merlin

    queries = {
        'red':     'http://host/v1/landsat/chip-specs?q=tags:red AND sr',
        'green':   'http://host/v1/landsat/chip-specs?q=tags:green AND sr',
        'blue':    'http://host/v1/landsat/chip-specs?q=tags:blue AND sr',
        'quality': 'http://host/v1/landsat/chip-specs?q=tags:pixelqa'}

    data = timeseries.create(
                      point=(123, 456),
                      acquired='1980-01-01/2015-12-31',
                      dates_fn=partial(functions.chexists,
                                       check_fn=timeseries.symmetric_dates,
                                       keys=['quality',]),
                      keyed_specs=chip_specs.getmulti(queries),
                      chips_fn=partial(chips.get, url='http://host/v1/landsat/chips'))

Retrieve Chips & Specs
----------------------

.. code-block:: python3

    from merlin.chips      import get as chips_fn
    from merlin.chip_specs import getmulti as specs_fn
    from merlin.composite  import chips_and_specs

    queries = {
        'red':   'http://host/v1/landsat/chip-specs?q=tags:red AND sr',
        'green': 'http://host/v1/landsat/chip-specs?q=tags:green AND sr',
        'blue':  'http://host/v1/landsat/chip-specs?q=tags:blue AND sr'}

    cas = chips_and_specs(point=(123, 456),
                          acquired='1980-01-01/2017-08-22',
                          keyed_specs=specs_fn(queries),
                          chips_fn=partial(chips_fn, url='http://host/v1/landsat/chips'))

    
