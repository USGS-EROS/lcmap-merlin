Develop
=======

Get The Source
--------------
.. code-block:: bash

    $ git clone git@github.com:usgs-eros/lcmap-merlin

    # Highly recommend working within a virtual environment
    $ conda create --name merlin python=3.6
    $ source activate merlin
    $ cd lcmap-merlin
    $ pip install -e .[test, dev, doc]


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

Build Sphinx Docs
-----------------
This is only necessary during development.  Release documents are built
automatically by readthedocs.io.

.. code-block:: bash

    $ cd docs
    $ make html
