import os

CWD = os.path.dirname(os.path.realpath(__file__))

def data_config():
    """ Controls the test data that is loaded into the system """
    return {'x': -1821585,
            'y': 2891595,
            'acquired': '1982-01-01/2015-12-12',
            'dataset_name': 'ARD',
            'chips_dir': os.path.join(CWD, 'data/chips'),
            'specs_dir': os.path.join(CWD, 'data/specs')}
