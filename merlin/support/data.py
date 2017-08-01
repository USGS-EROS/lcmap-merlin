"""
Functions for working with local data.
This module allows merlin functions to test using local data rather than
requiring external systems such as aardvark to be available.

Mock servers (such as aardvark) live in other modules, not here.

There are functions contained for updating the data that lives under
merlin/support/data.  The locations of this data is controlled by values
in merlin/support/__init__.py
"""

from merlin import chips as mc
from merlin import chip_specs as mcs
from merlin import functions as f
from merlin import files
from merlin import support
from urllib.parse import urlparse

import glob
import json
import os
import re


CHIPS_DIR = support.data_config()['chips_dir']
SPECS_DIR = support.data_config()['specs_dir']


def chips(spectra, root_dir=CHIPS_DIR):
    """Return chips for named spectra
    :param spectra: red, green, blue, nir, swir1, swir2, thermal or cfmask
    :type spectra: string
    :returns: sequence of chips
    """
    path = ''.join([root_dir, os.sep, '*', spectra, '*'])
    filenames = glob.glob(path)
    chips = [json.loads(files.read(filename)) for filename in filenames]
    return tuple(f.flatten(chips))


def chip_specs(spectra, root_dir=SPECS_DIR):
    """Returns chip specs for the named spectra.
    :param spectra: red, green, blue, nir, swir1, swir2, thermal or cfmask
    :type spectra: string
    :returns: sequence of chip specs
    """
    path = ''.join([root_dir, os.sep, '*', spectra, '*'])
    filenames = glob.glob(path)
    return json.loads(files.read(filenames[0]))


def chip_ids(root_dir=CHIPS_DIR):
    """Returns chip ids for available chip data in root_dir
    :param root_dir: directory where band data resides
    :return: tuple of tuples of chip ids (UL coordinates)
    """
    def getxy(fpath):
        _fs = fpath.split('_')
        return _fs[1], _fs[2]

    glob_exp = ''.join([root_dir, os.sep, '*blue*'])
    return tuple({getxy(i) for i in glob.glob(glob_exp)})


def spectra_index(specs):
    """Returns a dict keyed by ubid that maps to the spectra name
    :param specs: A dict of spectra: chip_specs
    :returns: A dict of ubid: spectra
    """
    def rekey_by_ubid(chip_spec, spectra):
        return dict((ubid, spectra) for ubid in mcs.ubids(chip_spec))

    return f.merge([rekey_by_ubid(cs, s) for s, cs in specs.items()])


def spectra_from_specfile(filename):
    """Returns the spectra the named chip spec file is associated with"""
    return os.path.basename(filename).split('_')[0]


def spec_query_id(url):
    """Generates identifier for spec query url based on the querystring"""
    return re.compile('[: =]').sub('_', urlparse(url).query)


def spec_query_ids(specs_url):
    """Returns the query portion of the chip_spec_url keyed to its spectra"""
    return {k: spec_query_id(v)
            for k, v in test.chip_spec_urls(specs_url).items()}


def spectra_from_queryid(queryid, root_dir=SPECS_DIR):
    """Returns the spectra name for a chip spec from the supplied queryid"""
    path = ''.join([root_dir, os.sep, '*', queryid, '*'])
    filenames = glob.glob(path)
    return [os.path.basename(filename).split('_')[0] for filename in filenames]


def test_specs(root_dir=SPECS_DIR):
    """Returns a dict of all test chip specs keyed by spectra
    :returns: sequence of chip specs
    """
    #fileid = lambda filename: os.path.splitext(os.path.basename(filename))[0]
    path = ''.join([root_dir, os.sep, '*'])
    fnames = glob.glob(path)
    #return {fileid(f): json.loads(files.read(f)) for f in filenames}
    return {spectra_from_specfile(f): json.loads(files.read(f)) for f in fnames}


def live_specs(specs_url):
    """Returns a dict of all chip specs defined by the driver.chip_spec_urls
    keyed by spectra"""
    return {k: mcs.get(v) for k, v in test.chip_spec_urls(specs_url).items()}


def update_specs(specs_url, conf=support.data_config()):
    """Updates the spec test data"""
    specs = live_specs(specs_url)
    qids = spec_query_ids(specs_url)

    for spectra in specs.keys():
        filename = '{}_{}.json'.format(spectra, qids[spectra])
        output_file = os.path.join(conf['specs_dir'], filename)
        files.write(files.mkdirs(output_file), json.dumps(specs[spectra]))


def update_chips(chips_url, specs_url, conf=support.data_config()):
    """Updates the chip test data"""
    x = conf['x']
    y = conf['y']
    dname = conf['dataset_name']
    acquired = conf['acquired']
    chips_dir = conf['chips_dir']
    specs = live_specs(specs_url)

    for spectra in specs.keys():
        filename = '{}_{}_{}_{}_{}.json'.format(spectra, x, y, dname,
                                                acquired.replace('/', '_'))
        output_file = os.path.join(chips_dir, filename)
        files.write(files.mkdirs(output_file),
                    json.dumps(mc.get(chips_url, x, y, acquired,
                                      mcs.ubids(specs[spectra]))))
