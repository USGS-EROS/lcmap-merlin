merlin.support
===============
.. automodule:: merlin.support
    :members:
    :undoc-members:


merlin.support.data
===================
.. automodule:: merlin.support.data
    :members: live_specs, spec_query_ids, spec_query_id, spectra_from_specfile, spectra_index
    :undoc-members:

    .. autofunction:: chips(spectra, support.data_config()['chips_dir'])

    .. autofunction:: chip_specs(spectra, root_dir=support.data_config()['specs_dir'])

    .. autofunction:: chip_ids(root_dir=support.data_config()['chips_dir'])

    .. autofunction:: spectra_from_queryid(queryid, root_dir=support.data_config()['specs_dir'])

    .. autofunction:: test_specs(root_dir=support.data_config()['specs_dir'])

    .. autofunction:: update_specs(specs_url, conf=support.data_config())

    .. autofunction:: update_chips(chips_url, specs_url, conf=support.data_config())


merlin.support.aardvark
=======================
.. automodule:: merlin.support.aardvark
    :members:
    :undoc-members:
