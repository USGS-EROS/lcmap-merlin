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
                                queries={'red': '?q=tags:red AND sr',
                                         'green': '?q=tags:green AND sr',
                                         'blue': '?q=tags:blue AND sr',
                                         'nir': '?q=tags:nir AND sr',
                                         'swir1': '?q=tags:swir1 AND sr',
                                         'swir2': '?q=tags:swir2 AND sr',
                                         'thermal': '?q=tags:thermal AND sr',
                                         'quality': '?q=quality AND sr'}),
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
