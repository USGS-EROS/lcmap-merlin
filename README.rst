.. image:: https://travis-ci.org/USGS-EROS/lcmap-merlin.svg?branch=develop
    :target: https://travis-ci.org/USGS-EROS/lcmap-merlin

.. image:: https://readthedocs.org/projects/lcmap-merlin/badge/?version=latest
    :target: http://lcmap-merlin.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Merlin
============
A Python3 library for turning LCMAP spatial data into timeseries like magic.


Features
--------
* Retrieve chips & chip specs
* Convert chips & chip specs into time series rods
* Many composable functions
* Built with efficiency in mind... leverages Numpy for heavy lifting.
* Tested with cPython 3.5 & 3.6


Example
-------
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


Documentation
-------------
Complete documentation is available at http://lcmap-merlin.readthedocs.io/


Installation
------------

.. code-block:: bash

   pip install lcmap-merlin


Get The Source
--------------
.. code-block:: bash

    $ git clone git@github.com:usgs-eros/lcmap-merlin

    # Highly recommend working within a virtual environment
    $ conda create --name merlin python=3.6
    $ source activate merlin
    $ cd lcmap-merlin
    $ pip install -e .[test]


Testing
-------

.. code-block:: bash

   $ pytest


Occasionally chip and chip spec test data may need to be updated if the source
specifications change.

Execute :code:`data.update_specs()` and :code:`data.update_chips()` from a repl.
The date range and spatial location of the data may be altered
in :code:`merlin/support/__init__.py`.  When expanding the data query date
range, please note that PyPi has a limit of 60MB per artifact.
Uploads exceeding this limit will result in failure messages while publishing.

.. code-block:: python3

   specs_url = 'http://localhost:5678/v1/landsat/chip-specs'
   chips_url = 'http://localhost:5678/v1/landsat/chips'

   from merlin.support import data
   data.update_specs(specs_url=specs_url)
   data.update_chips(chips_url=chips_url, specs_url=specs_url)

Versioning
----------
Merlin follows semantic versioning: http://semver.org/

License
-------
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to http://unlicense.org.
