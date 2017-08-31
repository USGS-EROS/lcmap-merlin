Cookbook
============

Create Timeseries
-------------------

.. code-block:: python3

    import merlin

    queries = {
        'red':   'http://host/landsat/v1/chip-specs?q=tags:red AND sr',
        'green': 'http://host/landsat/v1/chip-specs?q=tags:green AND sr',
        'blue':  'http://host/landsat/v1/chip-specs?q=tags:blue AND sr'}

    timeseries = merlin.create(point=(123, 456),
                               acquired='1980-01-01/2017-01-01',
                               queries=queries,
                               chips_url='http://host/landsat/v1/chips')

    print(timeseries)

    (((123, 456): {'red'  : [9, 8, 7 ...],
                   'green': [99, 88, 77 ...]},
                   'blue' : [12, 22, 33 ...],
                   'dates': ['2017-01-01', '2016-12-31', '2016-12-30' ...]}),
      (124, 456): {'red'  : [4, 3, 22 ...],
                   'green': [19, 8, 77 ...]},
                   'blue' : [1, 11, 3 ...],
                   'dates': ['2017-01-01', '2016-12-31', '2016-12-30' ...]}),)

Create Timeseries From Assymetric Data
--------------------------------------
.. code-block:: python3

    from functools import partial
    from merlin import chips
    from merlin import functions
    from merlin import timeseries
    import merlin

    queries = {
        'red':     'http://host/landsat/v1/chip-specs?q=tags:red AND sr',
        'green':   'http://host/landsat/v1/chip-specs?q=tags:green AND sr',
        'blue':    'http://host/landsat/v1/chip-specs?q=tags:blue AND sr',
        'quality': 'http://host/landsat/v1/chip-specs?q=tags:pixelqa'}

    data = timeseries.create(
                      point=(123, 456),
                      dates_fn=partial(functions.chexists,
                                       check_fn=timeseries.symmetric_dates,
                                       keys=['quality',]),
                      chips_url='http://localhost',
                      acquired='1980-01-01/2015-12-31',
                      queries=test.chip_spec_queries('http://localhost'))

Retrieve Chips & Specs
----------------------

.. code-block:: python3

    from merlin.chips      import get as chips_fn
    from merlin.chip_specs import get as specs_fn
    from merlin.composite  import chips_and_specs

    queries = {
        'red':   'http://host/landsat/v1/chip-specs?q=tags:red AND sr',
        'green': 'http://host/landsat/v1/chip-specs?q=tags:green AND sr',
        'blue':  'http://host/landsat/v1/chip-specs?q=tags:blue AND sr'}

    chips, specs = chips_and_specs(point=(123, 456),
                                   acquired='1980-01-01/2017-08-22',
                                   queries=queries,
                                   chips_fn=chips_fn,
                                   specs_fn=specs_fn,
                                   chips_url='http://host/landsat/v1/chips')
