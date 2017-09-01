Cookbook
============

Create Timeseries
-------------------

.. code-block:: python3

    import merlin

    queries = {
        'red':   'http://host/v1/landsat/chip-specs?q=tags:red AND sr',
        'green': 'http://host/v1/landsat/chip-specs?q=tags:green AND sr',
        'blue':  'http://host/v1/landsat/chip-specs?q=tags:blue AND sr'}

    timeseries = merlin.create(point=(123, 456),
                               acquired='1980-01-01/2017-01-01',
                               queries=queries,
                               chips_url='http://host/v1/landsat/chips')

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
                      dates_fn=partial(functions.chexists,
                                       check_fn=timeseries.symmetric_dates,
                                       keys=['quality',]),
                      chips_url='http://localhost',
                      acquired='1980-01-01/2015-12-31',
                      queries=queries)

Retrieve Chips & Specs
----------------------

.. code-block:: python3

    from merlin.chips      import get as chips_fn
    from merlin.chip_specs import get as specs_fn
    from merlin.composite  import chips_and_specs

    queries = {
        'red':   'http://host/v1/landsat/chip-specs?q=tags:red AND sr',
        'green': 'http://host/v1/landsat/chip-specs?q=tags:green AND sr',
        'blue':  'http://host/v1/landsat/chip-specs?q=tags:blue AND sr'}

    chips, specs = chips_and_specs(point=(123, 456),
                                   acquired='1980-01-01/2017-08-22',
                                   queries=queries,
                                   chips_fn=chips_fn,
                                   specs_fn=specs_fn,
                                   chips_url='http://host/v1/landsat/chips')
