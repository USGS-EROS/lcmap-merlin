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

Occasionally test data may need to be updated if source data changes.  Merlin uses the
vcrpy_ library to save HTTP requests for replay during testing.

.. _vcrpy: https://github.com/kevin1024/vcrpy

VCR cassettes are configured in ```test/__init__.py```.  To support multiple data source
versions, add new attributes to the module that correspond to the data source or data set version
to be tested against.

.. code-block:: python3

    import vcr as _vcr

    # chipmunk parameters for test data
    x = -2094585
    y = 1952805
    x_nodata = -183585.0
    y_nodata = 302805.0
    acquired = '2010/2013'
    profile = 'chipmunk-ard'
    env = {'CHIPMUNK_URL': 'http://localhost:5656'}
    ard-c1-v1-cassette = 'test/resources/chipmunk-ard-c1-v1-cassette.yaml'
    ard-c1-v2-cassette = 'test/resources/chipmunk-ard-c1-v2-cassette.yaml'
    aux-c1-v1-cassette = 'test/resources/chipmunk-aux-c1-v1-cassette.yaml'
    vcr = _vcr.VCR(record_mode='new_episodes')


Apply the proper decorator value to each function for the version under test.

.. code-block:: python3

    import test
    
    @test.vcr.use_cassette(test.ard-c1-v1-cassette)
    def test_some_func_c1_v1():
        assert awesomeness

    @test.vcr.use_cassette(test.ard-c1-v2-cassette)
    def test_some_func_c1_v2():
        assert awesomeness_v2


.. caution:: When expanding the ```acquired``` date range, keep in mind that PyPi has a limit of 60MB per artifact.  Uploads exceeding this limit will result in failure messages while publishing.


Build Sphinx Docs
-----------------
All Merlin docs are written in reStructuredText_.  All code comments are written using `Google Docstrings`_.

.. _Google Docstrings: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

Installing Sphinx and building the docs are only necessary during development.  Release documents are built automatically by readthedocs.io.

First, make sure you've installed Sphinx:

.. code-block:: bash

    $ pip install -e .[doc]

Automatically rebuild documentation and refresh the web browser when source files change:

.. code-block:: bash
                
    $ make autobuild

Manually build documentation one time:

.. code-block:: bash

    $ cd docs
    $ make html
