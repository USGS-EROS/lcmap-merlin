from cytoolz import assoc
from cytoolz import merge
from functools import partial
import chips
import chip_specs
import dates
# import formats
import os


def profiles(env, profile=None):
    __profiles = {
        'chipmunk-0.1-ard' : {
            'dates_fn': '',
            'chips_fn': partial(chipmunk.chips,
                                host=env.get('CHIPMUNK_HOST', None),
                                resource=env.get('CHIPMUNK_CHIPS_RESOURCE', '/chips')),
            'specs_fn': partial(chipmunk.specs,
                                host=env.get('CHIPMUNK_HOST', None),
                                resource=env.get('CHIPMUNK_SPECS_RESOURCE', '/specs'),
                                ubids={'red':     ['red', 'sr'],
                                       'green':   ['green', 'sr'],
                                       'blue':    ['blue', 'sr'],
                                       'nir':     ['nir', 'sr'],
                                       'swir1':   ['swir1', 'sr'],
                                       'swir2':   ['swir2', 'sr'],
                                       'thermal': ['thermal', 'sr'],
                                       'quality': ['quality', 'sr']}),
            'fmttr_fn': '',
            'snapr_fn': partial(chipmunk.snap,
                                host=env.get('CHIPMUNK_HOST', None),
                                resource=env.get('CHIPMUNK_SNAP_RESOURCE', '/grid/snap'))},
        'chipmunk-0.1-aux' : {
            'dates_fn': '',
            'chips_fn': '',
            'specs_fn': '',
            'fmttr_fn': '',
            'snapr_fn': '',
            'spec_queries': {'red': '?q=tags:red & SR'}},
        'local-ard': {
            'dates_fn': '',
            'chips_fn': '',
            'specs_fn': '',
            'fmttr_fn': '',
            'snapr_fn': ''},
        'local-aux': {
            'dates_fn': '',
            'chips_fn': '',
            'specs_fn': '',
            'fmttr_fn': '',
            'snapr_fn': ''}
        }
    
    return __profiles.get(profile, None) if profile else __profiles


def get(profile='chipmunk-0.1-ard', overrides=None):

    p = profiles(env=merge(os.environ, overrides if overrides else {}),
                 profile=profile)

    return assoc(p, 'profile', profile)
