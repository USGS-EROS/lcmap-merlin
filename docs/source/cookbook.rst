Cookbook
========

Configure Merlin For Chipmunk
-----------------------------
Merlin is configurable with environment variables and parameters.  Parameters override environment variables.

.. code-block:: python3

    import merlin
    import os

    # export CHIPMUNK_URL=http://localhost:5656/plus/path
    os.environ['CHIPMUNK_URL'] = 'http://localhost:5656/plus/path'

    merlin.cfg.get(profile='chipmunk-ard')

.. code-block:: python3

    import merlin

    merlin.cfg.get(profile='chipmunk-ard',
                   env={'CHIPMUNK_URL': 'http://localhost:5656/plus/path'})


View All Configuration Profiles
-------------------------------
Merlin configurations are organized into profiles, which group function implementations by use.
All profiles may be viewed by calling ```merlin.cfg.profiles``` with a ```None``` parameter.

.. code-block:: python3
                
    import merlin

    merlin.cfg.profiles(None)


Create Timeseries
-------------------

.. code-block:: python3

    import merlin

    timeseries = merlin.create(x=123,
                               y=456, 
                               acquired='1980-01-01/2017-01-01',
                               cfg=merlin.cfg.get('chipmunk-ard'))

    print(timeseries)

    (((123, 456, 123, 456), {'red'  : [9, 8, ...],
                             'green': [99, 88, ...]},
                             'blue' : [12, 22, ...],
                              'dates': ['2017-01-01', '2016-12-31', ...]}),
     ((123, 456, 124, 456), {'red'  : [4, 3, ...],
                             'green': [19, 8, ...]},
                             'blue' : [1, 11, ...],
                             'dates': ['2017-01-01', '2016-12-31', ...]}),)


Retrieve Chips
--------------

.. code-block:: python3

    import merlin
    
    fn = merlin.cfg.get('chipmunk-ard').get('chips_fn')
    
    fn(x=123, y=456, acquired='1980/2017', ubids=['LC08_SRB4', 'LE07_SRB3', ...])


Retrieve Specs
------------------

.. code-block:: python3

    import merlin

    fn = merlin.cfg.get('chipmunk-ard').get('registry_fn')

    fn()
    

Retrieve Specs Mapped To UBIDS
------------------------------

.. code-block:: python3

    import merlin

    registry = merlin.cfg.get('chipmunk-ard').get('registry_fn')
    
    merlin.specs.mapped(specs=registry(),
                        ubids=merlin.cfg.ubids.get('chipmunk-ard'))


Snap A Point To A Grid
----------------------
.. code-block:: python3
                
    import merlin
    
    fn = merlin.cfg.get('chipmunk-ard').get('snap_fn')
    
    fn(x=123, y=456)
