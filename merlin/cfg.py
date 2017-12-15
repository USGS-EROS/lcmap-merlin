from cytoolz import assoc
from cytoolz import merge
from functools import partial
from . import chipmunk
from . import chips
from . import dates
from . import formats
from . import specs
import os


def profiles(env, profile=None):
    __profiles = {
        'chipmunk-0.1-pyccd-ard' : {
            'grid_fn': partial(chipmunk.grid,
                               url=env.get('CHIPMUNK_URL', None),
                               resource=env.get('CHIPMUNK_GRID_RESOURCE', '/grid')),
            'dates_fn': dates.symmetric,
            'chips_fn': partial(chipmunk.chips,
                                url=env.get('CHIPMUNK_URL', None),
                                resource=env.get('CHIPMUNK_CHIPS_RESOURCE', '/chips')),
            'specs_fn': partial(specs.mapped,
                                ubids={'red':     ['LC08_SRB4',    'LE07_SRB3',    'LT05_SRB3',    'LT04_SRB3'],
                                       'green':   ['LC08_SRB3',    'LE07_SRB2',    'LT05_SRB2',    'LT04_SRB2'],
                                       'blue':    ['LC08_SRB2',    'LE07_SRB1',    'LT05_SRB1',    'LT04_SRB1'],
                                       'nir':     ['LC08_SRB5',    'LE07_SRB4',    'LT05_SRB4',    'LT04_SRB4'],
                                       'swir1':   ['LC08_SRB6',    'LE07_SRB5',    'LT05_SRB5',    'LT04_SRB5'],
                                       'swir2':   ['LC08_SRB7',    'LE07_SRB7',    'LT05_SRB7',    'LT04_SRB7'],
                                       'thermal': ['LC08_BTB10',   'LE07_BTB6',    'LT05_BTB6',    'LT04_BTB6'],
                                       'quality': ['LC08_PIXELQA', 'LE07_PIXELQA', 'LT05_PIXELQA', 'LT04_PIXELQA']}),
            'format_fn': formats.pyccd,
            'registry_fn': partial(chipmunk.registry,
                                   url=env.get('CHIPMUNK_URL', None),
                                   resource=env.get('CHIPMUNK_REGISTRY_PATH', '/registry')),
            'snap_fn': partial(chipmunk.snap,
                               url=env.get('CHIPMUNK_URL', None),
                               resource=env.get('CHIPMUNK_SNAP_RESOURCE', '/grid/snap'))},
        'chipmunk-0.1-aux' : {
            'dates_fn': '',
            'chips_fn': '',
            'specs_fn': '',
            'fmttr_fn': '',
            'snapr_fn': '',
            'spec_queries': {''}},
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
